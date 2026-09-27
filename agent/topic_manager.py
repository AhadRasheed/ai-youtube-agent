def get_topic():
    print("\n1. Enter a topic manually")
    print("2. Automatic trend discovery (future provider)")
    choice=input("\nChoose 1 or 2: ").strip()
    if choice=="2":
        print("\nAutomatic trend discovery is not enabled in this V1.")
        return ""
    return input("\nEnter video topic: ").strip()
