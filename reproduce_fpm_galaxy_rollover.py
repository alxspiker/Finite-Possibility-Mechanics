import argparse
import numpy as np
import os
import csv
import json

# ==========================================
# Finite Possibility Mechanics Harness
# Executable Falsification Blade
# ==========================================

# Core Constants
G_CONST = 4.3009e-6  # kpc (km/s)^2 / M_sun

def fpm_v(r, R_c, r_c, R_d, V_inf, V_core):
    """
    FPM non-linear field equation analytical approximation for finite disk geometry.
    """
    r = np.array(r, dtype=float)
    GDO_d = V_inf**2
    GDO_c = V_core**2
    
    g = (GDO_c / R_c) * np.exp(-r / R_c) + (GDO_d * R_d) / ((r + r_c) * (r + r_c + R_d))
    return np.sqrt(r * g)

# ==========================================
# Baseline Evaluation Hooks
# ==========================================
def evaluate_baryon_newtonian(r, mass_profile):
    """Placeholder hook for strictly Newtonian (baryon-only) predictions."""
    pass

def evaluate_mond(r, mass_profile, a0):
    """Placeholder hook for Modified Newtonian Dynamics (MOND) interpolation predictions."""
    pass

def evaluate_nfw_halo(r, m200, c200):
    """Placeholder hook for Navarro-Frenk-White (NFW) dark matter halo predictions."""
    pass

# ==========================================
# Falsification Generation
# ==========================================
def generate_falsification_target(name, R_c, r_c, R_d, V_inf, V_core):
    """
    Generates the strict, testable far-field rollover falsification target for a given galaxy.
    Does NOT require or use observed far-field velocity data.
    """
    v30 = fpm_v(30, R_c, r_c, R_d, V_inf, V_core)
    v240 = fpm_v(240, R_c, r_c, R_d, V_inf, V_core)
    
    ratio = v240 / v30
    
    far_field = np.linspace(240, 2400, 100)
    slope = np.polyfit(np.log(far_field), np.log(fpm_v(far_field, R_c, r_c, R_d, V_inf, V_core)), 1)[0]
    
    # Establish prospective failure criteria
    acceptable_slope_band = (-0.60, -0.40) # Must align with Keplerian decline -0.5
    acceptable_ratio_band = (ratio - 0.1, ratio + 0.1) # Must exhibit the physical amplitude drop
    
    return {
        "Galaxy": name,
        "Disk Scale (R_d)": R_d,
        "Expected Rollover Radius": R_d * 2, # Begins significant decline past ~2 R_d
        "Predicted v(240)/v(30) Ratio": ratio,
        "Predicted Far-Field Slope": slope,
        "Failure Criteria (Slope)": acceptable_slope_band,
        "Failure Criteria (Ratio)": acceptable_ratio_band
    }

def run_synthetic_demo():
    print("=== FPM SYNTHETIC DEMO MODE ===")
    print("Generating pure prospective prediction targets without far-field data fitting.\n")
    
    # Synthetic Galaxy (e.g. NGC 3198 structural analog)
    target = generate_falsification_target("SYNTH-3198", 2.0, 0.3, 120.0, 220.0, 100.0)
    
    print("| Galaxy | Baryonic Disk Scale | Predicted Rollover Radius | Predicted v(240)/v(30) | Predicted Far-Field Slope | Failure Condition (Slope) | Failure Condition (Ratio) |")
    print("|--------|--------------------:|--------------------------:|-----------------------:|--------------------------:|--------------------------:|--------------------------:|")
    print(f"| {target['Galaxy']} | {target['Disk Scale (R_d)']:.1f} kpc | ~{target['Expected Rollover Radius']:.1f} kpc | {target['Predicted v(240)/v(30) Ratio']:.4f} | {target['Predicted Far-Field Slope']:.4f} | Not in {target['Failure Criteria (Slope)']} | Not in ({target['Failure Criteria (Ratio)'][0]:.4f}, {target['Failure Criteria (Ratio)'][1]:.4f}) |")
    
    print("\n[!] Parameter Freeze Metadata: SYNTH-3198 [R_c=2.0, r_c=0.3, R_d=120.0, V_inf=220.0, V_core=100.0]")
    print("[!] Action: FPM prediction is fully locked. Awaiting far-field observations or weak-lensing data for empirical execution.")

def run_real_predictions(input_file):
    print("=== FPM REAL PREDICTION MODE ===")
    print(f"Loading locked structural input data from: {input_file}")
    
    if not os.path.exists(input_file):
        print(f"\n[ERROR] File not found: {input_file}")
        print("To run the coronation test, you must provide a locked CSV of baryonic profiles.")
        print("Required CSV columns: Galaxy_Name, R_c, r_c, R_d, V_inf, V_core")
        return

    targets = []
    with open(input_file, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            target = generate_falsification_target(
                row['Galaxy_Name'], 
                float(row['R_c']), 
                float(row['r_c']), 
                float(row['R_d']), 
                float(row['V_inf']), 
                float(row['V_core'])
            )
            targets.append(target)
            
    print("\n| Galaxy | Baryonic Disk Scale | Predicted Rollover Radius | Predicted v(240)/v(30) | Predicted Far-Field Slope | Failure Condition (Slope) |")
    print("|--------|--------------------:|--------------------------:|-----------------------:|--------------------------:|--------------------------:|")
    for t in targets:
        print(f"| {t['Galaxy']} | {t['Disk Scale (R_d)']:.1f} kpc | ~{t['Expected Rollover Radius']:.1f} kpc | {t['Predicted v(240)/v(30) Ratio']:.4f} | {t['Predicted Far-Field Slope']:.4f} | Not in {t['Failure Criteria (Slope)']} |")
        
    print("\n[!] Predictions locked. Outputting execution artifacts...")
    # Reserved for future logging of prediction JSON and Git commit hashes

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="FPM Galactic Rollover Falsification Harness")
    parser.add_argument("--demo-synthetic", action="store_true", help="Run the math demonstration on a synthetic parameter set.")
    parser.add_argument("--predict-real", type=str, metavar="INPUT_CSV", help="Generate locked rollover predictions for real galaxies based on their baryonic structure.")
    
    args = parser.parse_args()
    
    if args.predict_real:
        run_real_predictions(args.predict_real)
    elif args.demo_synthetic:
        run_synthetic_demo()
    else:
        parser.print_help()
