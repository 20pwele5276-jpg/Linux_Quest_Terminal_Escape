from app.missions import MISSIONS


# Simulated files and directories inside the game.
GAME_FILES = {
    "intel.txt": "INTEL: The escape code is LINUX-QUEST.",
}

GAME_DIRECTORIES = {".", "secret"}
GAME_FILES_CREATED = set()


def reset_game_world():
    """Reset the simulated filesystem for a new game."""
    global GAME_FILES, GAME_DIRECTORIES, GAME_FILES_CREATED

    GAME_FILES = {
        "intel.txt": "INTEL: The escape code is LINUX-QUEST.",
    }

    GAME_DIRECTORIES = {".", "secret"}
    GAME_FILES_CREATED = set()


def get_mission(mission_id):
    """Return a mission using its ID."""
    return next(
        (mission for mission in MISSIONS if mission["id"] == mission_id),
        None,
    )


def execute_game_command(command):
    """Simulate supported Linux commands without running them on Ubuntu."""

    command = command.strip()
    parts = command.split()

    if not parts:
        return "Enter a command."

    name = parts[0]

    if name == "ls":
        items = sorted(
            set(GAME_FILES)
            | GAME_DIRECTORIES
            | GAME_FILES_CREATED
        )
        return "  ".join(items)

    if name == "pwd":
        return "/home/player"

    if name == "cat":
        if len(parts) != 2:
            return "Usage: cat filename"

        filename = parts[1]

        if filename in GAME_FILES:
            return GAME_FILES[filename]

        if filename in GAME_FILES_CREATED:
            return ""

        return f"cat: {filename}: No such file"

    if name == "cd":
        if len(parts) != 2:
            return "Usage: cd directory"

        directory = parts[1]

        if directory in GAME_DIRECTORIES:
            return f"Directory changed to {directory}"

        return f"cd: {directory}: No such directory"

    if name == "mkdir":
        if len(parts) != 2:
            return "Usage: mkdir directory"

        directory = parts[1]

        if directory in GAME_DIRECTORIES:
            return f"mkdir: {directory}: Already exists"

        GAME_DIRECTORIES.add(directory)
        return f"Directory created: {directory}"

    if name == "touch":
        if len(parts) != 2:
            return "Usage: touch filename"

        filename = parts[1]

        if filename not in GAME_FILES:
            GAME_FILES_CREATED.add(filename)

        return f"File created: {filename}"

    if name == "cp":
        if len(parts) != 3:
            return "Usage: cp source destination"

        source, destination = parts[1], parts[2]

        if source not in GAME_FILES and source not in GAME_FILES_CREATED:
            return f"cp: {source}: No such file"

        if source in GAME_FILES:
            GAME_FILES[destination] = GAME_FILES[source]
        else:
            GAME_FILES_CREATED.add(destination)

        return f"File copied to {destination}"

    if name == "mv":
        if len(parts) != 3:
            return "Usage: mv source destination"

        source, destination = parts[1], parts[2]

        if source not in GAME_FILES and source not in GAME_FILES_CREATED:
            return f"mv: {source}: No such file"

        if destination.endswith("/"):
            directory = destination.rstrip("/")

            if directory not in GAME_DIRECTORIES:
                return f"mv: {directory}: No such directory"

            filename = source.split("/")[-1]
            destination = f"{directory}/{filename}"

        if source in GAME_FILES:
            GAME_FILES[destination] = GAME_FILES.pop(source)
        else:
            GAME_FILES_CREATED.discard(source)
            GAME_FILES_CREATED.add(destination)

        GAME_FILES_CREATED.discard(source)
        return f"File moved to {destination}"

    if name == "ps":
        return "PID  COMMAND\n101  secure-server\n204  firewall"

    if name == "echo":
        return command[5:] if command.startswith("echo ") else ""

    if name == "clear":
        return "__CLEAR__"

    if name == "help":
        return "Commands: ls, pwd, cat, cd, mkdir, touch, cp, mv, ps, echo, clear"

    return f"{name}: command not available in this game."


def check_command(mission_id, user_command):
    """Check whether the command completes the active mission."""

    mission = get_mission(mission_id)

    if mission is None:
        return {
            "success": False,
            "message": "MISSION NOT FOUND.",
            "points": 0,
        }

    command = user_command.strip()

    if command != mission["expected_command"]:
        return {
            "success": False,
            "message": "ACCESS DENIED! Incorrect command.",
            "points": 0,
        }

    output = execute_game_command(command)

    if output.startswith(("cat:", "cd:", "mkdir:", "cp:", "mv:")):
        return {
            "success": False,
            "message": output,
            "points": 0,
        }

    return {
        "success": True,
        "message": mission["success_message"],
        "points": mission["points"],
        "output": output,
    }
