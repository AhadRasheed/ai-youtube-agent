def request_approval(metadata,video_path):
    print("\n==============================")
    print("VIDEO READY FOR APPROVAL")
    print("==============================")
    print("Title:",metadata.get("title",""))
    print("Video:",video_path)
    return input("\nApprove upload? [Y/N] > ").strip().lower()=="y"
