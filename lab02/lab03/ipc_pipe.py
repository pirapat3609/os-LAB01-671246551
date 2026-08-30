# ipc_pipe.py
import os
import time


def main():
    # Ask the OS to create a unidirectional communication channel
    # r = File descriptor for reading
    # w = File descriptor for writing
    r, w = os.pipe()

    pid = os.fork()

    if pid > 0:
        # --- PARENT PROCESS (Simulating ML Trainer) ---
        os.close(w)

        r_file = os.fdopen(r)

        print(f"[Trainer PID:{os.getpid()}] Waiting for data from DataLoader...")

        data = r_file.read()

        print(f"[Trainer PID:{os.getpid()}] Received Data: '{data}'")
        print(f"[Trainer PID:{os.getpid()}] Training complete.")

        os.wait()

    elif pid == 0:
        # --- CHILD PROCESS (Simulating DataLoader) ---
        os.close(r)

        w_file = os.fdopen(w, 'w')

        print(f" -> [DataLoader PID:{os.getpid()}] Loading image from disk...")

        time.sleep(2)

        image_data = "Image_Tensor_Batch_01"

        print(f" -> [DataLoader PID:{os.getpid()}] Sending data through OS Pipe...")

        w_file.write(image_data)

        w_file.close()


if __name__ == "__main__":
    main()
    