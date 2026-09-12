from cx_Freeze import setup, Executable

build_exe_options = {
    "packages": ["os", "json", "threading", "tkinter", "pyautogui", "keyboard"],
    "excludes": [],
}

bdist_msi_options = {
    "add_to_path": False,
    "all_users": False,
    "initial_target_dir": r"[ProgramFiles64Folder]\AntiAFK",
}

setup(
    name="Anti-AFK",
    version="1.0.0",
    description="Universal Anti-AFK Tool",
    options={
        "build_exe": build_exe_options,
        "bdist_msi": bdist_msi_options
    },
    executables=[
        Executable(
            script="Anti-afk.py", 
            base="gui",
            target_name="AntiAFK.exe"
        )
    ]
)