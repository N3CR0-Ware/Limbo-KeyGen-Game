from shutil import which
import subprocess
import threading
from time import sleep
from server import main

python_path = which("python")
python3_path = which("python3")
if (python3_path is None) or (python_path and (("WindowsApps" in python3_path) or ("mingw64" in python3_path))):
    cmd = "python"
else:
    cmd = "python3"

counted = 0
counted_lock = threading.Lock()

threading.Thread(target=main, daemon=True).start()


def launch_client(client_number: int) -> None:
    global counted
    result = subprocess.run([cmd, "key.py"])
    if result.returncode != 0:
        print(f"[main] client window #{client_number} exited with code {result.returncode} "
              f"(check for a missing key{{0-7}}.png, config.json, or a crash inside key.py)")
    with counted_lock:
        counted -= 1


for client_number in range(8):
    with counted_lock:
        counted += 1
    threading.Thread(target=launch_client, args=(client_number,), daemon=True).start()
    sleep(0.23)

while True:
    with counted_lock:
        if counted <= 0:
            break
    sleep(0.1)
