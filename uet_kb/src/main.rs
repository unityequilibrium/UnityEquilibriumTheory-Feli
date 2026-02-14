mod db;
mod mcp;

use uet_core::parameters::get_params;
use uet_core::fields::Field;
use uet_core::dynamics::compute_omega;
use ndarray::ArrayD;
use clap::{Parser, Subcommand};
use std::path::Path;

#[derive(Parser)]
#[command(name = "uet_kb")]
#[command(about = "UET Knowledge Base Server (Rust + Postgres)", long_about = None)]
struct Cli {
    #[arg(short, long, default_value = "postgres://postgres:postgres@localhost:5432/uet_kb")]
    db_url: String,

    #[command(subcommand)]
    command: Option<Commands>,
}

#[derive(Subcommand)]
enum Commands {
    /// Test the physics engine core
    TestPhysics,
    /// Initialize the database (Install extensions & Tables)
    InitDb,
    /// Ingest a text file (Fake embedding for now)
    Ingest {
        #[arg(short, long)]
        file: String,
    },
    /// Search for concepts
    Search {
        #[arg(short, long)]
        query: String,
    },
    /// Start the MCP JSON-RPC Server
    StartMcpServer,
}

#[tokio::main]
async fn main() {
    let cli = Cli::parse();

    match &cli.command {
        Some(Commands::TestPhysics) => {
            println!("Testing UET Physics Core integration...");
            // ... (Physics code remains mostly synchronous logic, but running in async runtime is fine)
            let params = get_params("electroweak").unwrap();
            println!("Loaded Parameters: Scale={}, Kappa={}", params.scale, params.kappa);
            
            let shape = vec![10];
            let data = ArrayD::from_elem(shape, params.c0 + 0.1);
            let field = Field::new(data);
            
            let omega = compute_omega(&field, None, 0.1, &params);
            println!("Computed Omega: {}", omega);
            println!("✅ Integration successful!");
        }
        Some(Commands::InitDb) => {
            println!("Initializing database at: {}", cli.db_url);
            match db::init_db(&cli.db_url).await {
                Ok(_) => println!("✅ Database initialized (pgvector enabled)."),
                Err(e) => eprintln!("❌ Error: {}", e),
            }
        }
        Some(Commands::Ingest { file }) => {
            println!("Ingesting file: {}", file);
            // Connect to DB
            let pool = match db::init_db(&cli.db_url).await {
                Ok(p) => p,
                Err(e) => {
                    eprintln!("❌ Failed to connect/init DB: {}", e);
                    return;
                }
            };
            
            // Read Content
            let content = if Path::new(file).exists() {
                std::fs::read_to_string(file).expect("Failed to read file")
            } else {
                file.clone() // Treat as raw text
            };

            // Insert Doc
            let doc_id = db::insert_document(&pool, None, file, &content, None).await.expect("Failed to insert doc");
            println!("Created Document ID: {}", doc_id);

            // Mock Chunking & Embedding
            let chunks = content.split('\n').filter(|s| !s.trim().is_empty());
            for (_i, chunk_text) in chunks.enumerate() {
                // Mock Embedding: use 1024 for semantic, 20 for physics
                let s_vec = vec![0.0; 1024]; 
                let p_vec = vec![0.0; 20];

                db::insert_chunk(&pool, &doc_id, chunk_text, &s_vec, &p_vec).await.expect("Failed to insert chunk");
            }
            println!("✅ Ingestion complete.");
        }
        Some(Commands::Search { query }) => {
            println!("Searching for: '{}'", query);
             let pool = match db::init_db(&cli.db_url).await {
                Ok(p) => p,
                Err(e) => {
                    eprintln!("❌ Failed to connect/init DB: {}", e);
                    return;
                }
            };
            
            // Query Embedding (Mock 1024d)
            let vec = vec![0.0; 1024]; 
            
            // Top K = 5
            match db::search_similar(&pool, &vec, 5).await {
                Ok(results) => {
                    for res in results {
                        println!("- [Score: {:.4}] (Doc: {}) {}", res.score, res.path, res.text.trim());
                    }
                }
                Err(e) => eprintln!("❌ Search failed: {}", e),
            }
        }
        Some(Commands::StartMcpServer) => {
            if let Err(e) = mcp::run_mcp_server(&cli.db_url).await {
                eprintln!("MCP Server Error: {}", e);
            }
        }
        None => {
            println!("UET Knowledge Base Server v0.1.0 (Postgres Edition)");
            println!("Use --help for commands.");
        }
    }
}
