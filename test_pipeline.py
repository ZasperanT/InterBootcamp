from src.pipeline import process_meeting


audio_path = "ES2002a.Mix-Headset.wav"


result = process_meeting(audio_path)


print("\n================================")
print("PIPELINE COMPLETE")
print("================================")

print("\nRaw transcript characters:")
print(len(result["raw_transcript"]))

print("\nRefined transcript characters:")
print(len(result["refined_transcript"]))

print("\nMeeting record:")
print(result["meeting_record"])