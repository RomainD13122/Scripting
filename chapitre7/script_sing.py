import time
import sys

def main():
    while True:
        try:
            print("Travail en cours... (CTRL-C pour menu)")
            time.sleep(1) 
        except KeyboardInterrupt:
            choice = input("\n[Menu] (R)epos 10s / (C)ontinuer / (Q)uitter : ").lower()
            if choice == 'r':
                print("Repos de 10s...")
                time.sleep(10)
            elif choice == 'q':
                print("Fermeture...")
                break
            elif choice == 'c':
                print("Reprise...")
                continue
            else:
                print("Choix invalide, reprise par défaut.")
if __name__ == "__main__":
    main()