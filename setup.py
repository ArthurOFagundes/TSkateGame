import cx_Freeze

executables = [cx_Freeze.Executable(
    script="skategame.py", icon="images/TskateIcon.png")]

cx_Freeze.setup(
    name="Skate Game",
    options={"build_exe": {"packages": ["pygame"],
                           "include_files": ["images", "sounds"]
                           }},
    executables=executables
)
