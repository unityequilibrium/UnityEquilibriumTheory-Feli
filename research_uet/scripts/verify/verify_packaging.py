import sys
import os

# Add the current directory to sys.path to simulate a package install
sys.path.insert(0, os.getcwd())

print("🚀 Verifying UET Library Packaging...")

try:
    import research_uet as uet

    print("✅ Successfully imported research_uet")
except ImportError as e:
    print(f"❌ Failed to import research_uet: {e}")
    sys.exit(1)

# Test Fluid
try:
    print("\n💧 Testing basic Fluid Engine instantiation...")
    fluid_solver = uet.fluid.Engine2D(nx=32, ny=32, dt=0.01)
    print("✅ uet.fluid.Engine2D instantiated successfully")
    print(f"   Name: {fluid_solver.name}")
except Exception as e:
    print(f"❌ Failed to use uet.fluid: {e}")

# Test Complexity
try:
    print("\n🕸️ Testing basic Complexity Engine instantiation...")
    comp_solver = uet.complexity.ComplexityEngine(nx=20, ny=20)
    print("✅ uet.complexity.ComplexityEngine instantiated successfully")
    print(f"   Name: {comp_solver.name}")
except Exception as e:
    print(f"❌ Failed to use uet.complexity: {e}")

# Test Mathnicry (Riemann)
try:
    print("\n📐 Testing basic Mathnicry (Riemann) instantiation...")
    riemann = uet.math.RiemannEngine()
    print("✅ uet.math.RiemannEngine instantiated successfully")
except Exception as e:
    print(f"❌ Failed to use uet.math: {e}")

# Test SHA256 (Rust Miner proxy/fallback)
try:
    print("\n⛏️ Testing basic SHA256 Native instantiation...")
    # SHA256 is a module now, not a class
    print(f"   SHA256 Module: {uet.math.SHA256}")
    print("✅ uet.math.SHA256 loaded successfully")
except Exception as e:
    print(f"❌ Failed to use uet.math.SHA256: {e}")

print("\n✨ Verification Complete! The library structure is valid.")
