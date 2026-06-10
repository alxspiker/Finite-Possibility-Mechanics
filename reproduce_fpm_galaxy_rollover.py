import argparse
import numpy as np
import os
import csv
import hashlib
import subprocess

# ==========================================
# Finite Possibility Mechanics Harness
# Executable Falsification Blade
# Script Version: v1.1-Falsification
# ==========================================

G_CONST = 4.3009e-6  # kpc (km/s)^2 / M_sun

def get_git_revision_hash():
    try:
        return subprocess.check_output(['git', 'rev-parse', 'HEAD'], stderr=subprocess.STDOUT).decode('ascii').strip()
    except Exception:
        return "UNKNOWN_COMMIT (Not a git repository or git not installed)"

def hash_file(filepath):
    """Generate SHA-256 hash of the input structural data file to guarantee lock."""
    h = hashlib.sha256()
    with open(filepath, 'rb') as file:
        while chunk := file.read(8192):
            h.update(chunk)
    return h.hexdigest()

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
# (To be invoked during the separate EVALUATION phase)
# ==========================================
def evaluate_baryon_newtonian(r, mass_profile):
    """Reserved for future evaluation script. Must compute standard Newton gravity from baryon map."""
    pass

def evaluate_mond(r, mass_profile, a0):
    """Reserved for future evaluation script. Must compute standard MOND interpolation."""
    pass

def evaluate_nfw_halo(r, m200, c200):
    """Reserved for future evaluation script. Must compute standard NFW halo fit."""
    pass

# ==========================================
# Falsification Generation
# ==========================================
def generate_falsification_target(name, R_c, r_c, R_d, V_inf, V_core):
    """
    Generates the strict, testable far-field rollover falsification target.
    GUARANTEE: Does NOT require, read, or use observed far-field velocity data.
    """
    v30 = fpm_v(30, R_c, r_c, R_d, V_inf, V_core)
    v240 = fpm_v(240, R_c, r_c, R_d, V_inf, V_core)
    
    ratio = v240 / v30
    
    far_field = np.linspace(240, 2400, 100)
    slope = np.polyfit(np.log(far_field), np.log(fpm_v(far_field, R_c, r_c, R_d, V_inf, V_core)), 1)[0]
    
    acceptable_slope_band = (-0.60, -0.40) 
    acceptable_ratio_band = (ratio - 0.1, ratio + 0.1) 
    
    return {
        "Galaxy": name,
        "Disk Scale (R_d)": R_d,
        "Expected Rollover Radius": R_d * 2, 
        "Predicted v(240)/v(30) Ratio": ratio,
        "Predicted Far-Field Slope": slope,
        "Failure Criteria (Slope)": acceptable_slope_band,
        "Failure Criteria (Ratio)": acceptable_ratio_band,
        "Parameters": f"R_c={R_c}, r_c={r_c}, R_d={R_d}, V_inf={V_inf}, V_core={V_core}"
    }

def print_metadata(input_hash=None):
    print("\n==============================================")
    print("FPM PROSPECTIVE PREDICTION INFRASTRUCTURE")
    print("==============================================")
    print(f"Script Version : v1.1-Falsification")
    print(f"Git Commit Hash: {get_git_revision_hash()}")
    if input_hash:
        print(f"Input File Hash: {input_hash} (SHA-256)")
    print("Constraint     : ZERO observed far-field velocity data used in this prediction pass.")
    print("==============================================\n")

def run_synthetic_demo():
    print_metadata()
    print("=== SYNTHETIC DEMONSTRATOR MODE ===")
    
    target = generate_falsification_target("SYNTHETIC-MW/NGC3198-ANALOG", 2.0, 0.3, 120.0, 220.0, 100.0)
    
    print(f"[!] Parameter Freeze Metadata: {target['Galaxy']} [{target['Parameters']}]\n")
    print("| Galaxy | Baryonic Disk Scale | Predicted Rollover Radius | Predicted v(240)/v(30) | Predicted Far-Field Slope | Failure Condition (Slope) | Failure Condition (Ratio) |")
    print("|--------|--------------------:|--------------------------:|-----------------------:|--------------------------:|--------------------------:|--------------------------:|")
    print(f"| {target['Galaxy']} | {target['Disk Scale (R_d)']:.1f} kpc | ~{target['Expected Rollover Radius']:.1f} kpc | {target['Predicted v(240)/v(30) Ratio']:.4f} | {target['Predicted Far-Field Slope']:.4f} | Not in ({target['Failure Criteria (Slope)'][0]:.2f}, {target['Failure Criteria (Slope)'][1]:.2f}) | Not in ({target['Failure Criteria (Ratio)'][0]:.4f}, {target['Failure Criteria (Ratio)'][1]:.4f}) |")
    
    print("\n[!] Action: Prospective FPM prediction is fully locked. Awaiting independent empirical evaluation.")

def run_real_predictions(input_file):
    if not os.path.exists(input_file):
        print(f"\n[ERROR] File not found: {input_file}")
        return

    file_hash = hash_file(input_file)
    print_metadata(input_hash=file_hash)
    
    print("=== REAL PREDICTION PIPELINE ===")
    print(f"Loading locked structural input data from: {input_file}")

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
            
    print("\n| Galaxy | Baryonic Disk Scale | Predicted Rollover Radius | Predicted v(240)/v(30) | Predicted Far-Field Slope | Failure Condition (Slope) | Parameters |")
    print("|--------|--------------------:|--------------------------:|-----------------------:|--------------------------:|--------------------------:|:-----------|")
    for t in targets:
        print(f"| {t['Galaxy']} | {t['Disk Scale (R_d)']:.1f} kpc | ~{t['Expected Rollover Radius']:.1f} kpc | {t['Predicted v(240)/v(30) Ratio']:.4f} | {t['Predicted Far-Field Slope']:.4f} | Not in ({t['Failure Criteria (Slope)'][0]:.2f}, {t['Failure Criteria (Slope)'][1]:.2f}) | {t['Parameters']} |")
        
    print("\n[!] Structural prospective predictions generation complete. Evaluation pipeline must be run completely separately.")

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
