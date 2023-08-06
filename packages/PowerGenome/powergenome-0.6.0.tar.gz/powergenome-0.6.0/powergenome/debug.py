from powergenome.run_powergenome_multiple_outputs_cli import main

main(
    # settings_file="/Users/greg/Documents/work/Princeton/bug testing systems/wilson wecc/wecc_settings.yml",
    # settings_file="/Users/greg/Documents/work/Princeton/bug testing systems/WECC_3Z_forgreg/settings.yml",
    settings_file="/Users/greg/Documents/work/Princeton/national-emm/settings_conus_3z",
    results_folder="test_outputs_identical",
    current_gens=True,
)
