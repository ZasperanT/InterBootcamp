import json
import tempfile
from datetime import datetime
from pathlib import Path

import streamlit as st

from src.pipeline import process_meeting


st.set_page_config(
    page_title="Meeting Assistant",
    page_icon="🎙️",
    layout="wide"
)


if "result" not in st.session_state:
    st.session_state.result = None

if "output_dir" not in st.session_state:
    st.session_state.output_dir = None

if "uploaded_filename" not in st.session_state:
    st.session_state.uploaded_filename = None


st.title("🎙️ Meeting Assistant")

st.write(
    "Upload a meeting recording and generate a refined transcript "
    "and structured meeting record."
)


uploaded_file = st.file_uploader(
    "Upload a meeting recording",
    type=[
        "wav",
        "mp3",
        "m4a",
        "mp4",
        "mpeg",
        "mpga",
        "webm"
    ]
)


if uploaded_file is not None:

    
    if st.session_state.uploaded_filename != uploaded_file.name:

        st.session_state.result = None
        st.session_state.output_dir = None
        st.session_state.uploaded_filename = uploaded_file.name

    st.success(
        f"File uploaded: {uploaded_file.name}"
    )



    if st.button(
        "▶ Start Processing",
        type="primary"
    ):

   
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=Path(uploaded_file.name).suffix
        ) as temp_file:

            temp_file.write(
                uploaded_file.getbuffer()
            )

            temp_audio_path = temp_file.name


     
        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        output_dir = (
            Path("outputs")
            / f"run_{timestamp}"
        )


        try:

            with st.status(
                "Processing meeting...",
                expanded=True
            ) as status:

                st.write(
                    "Validating audio..."
                )

                st.write(
                    "Transcribing meeting..."
                )

                st.write(
                    "Refining transcript..."
                )

                st.write(
                    "Generating meeting record..."
                )

                result = process_meeting(
                    temp_audio_path,
                    output_dir=str(output_dir)
                )


         
                st.session_state.result = result
                st.session_state.output_dir = output_dir


                status.update(
                    label="Meeting processing complete!",
                    state="complete",
                    expanded=False
                )


            st.success(
                "Meeting processing complete!"
            )


        except Exception as error:

            st.error(
                f"Processing failed: {error}"
            )

if st.session_state.result is not None:

    result = st.session_state.result

    meeting_record = result["meeting_record"]


    st.header("📋 Meeting Record")



    st.subheader("Summary")

    st.write(
        meeting_record["meeting_summary"]
    )

    st.subheader("Topics Discussed")

    for topic in meeting_record["topics_discussed"]:

        st.write(
            f"• {topic}"
        )


    st.subheader("Key Decisions")

    if meeting_record["key_decisions"]:

        for decision in meeting_record["key_decisions"]:

            st.write(
                f"• {decision['decision']}"
            )

    else:

        st.info(
            "No confirmed decisions."
        )



    st.subheader("Action Items")

    if meeting_record["action_items"]:

        for item in meeting_record["action_items"]:

            st.markdown(
                f"**Task:** {item['task']}"
            )

            st.markdown(
                f"**Owner:** {item['owner']}"
            )

            st.markdown(
                f"**Deadline:** {item['deadline']}"
            )

            st.divider()

    else:

        st.info(
            "No confirmed action items."
        )

    st.header("🔎 Evidence Verification")

    verification = result.get("verification")

    if verification is not None:

        for claim in verification["claims"]:

            if claim["status"] == "supported":
                status_label = "✅ Supported"
            elif claim["status"] == "contradicted":
                status_label = "❌ Contradicted"
            else:
                status_label = "⚠️ Uncertain"

            with st.expander(
                f"{claim['claim_id']} — {status_label}"
            ):

                st.write(
                    f"**Status:** {claim['status']}"
                )

                st.write(
                    f"**Reason:** {claim['reason']}"
                )

                st.write("**Evidence:**")

                if claim["evidence"]:

                    for evidence in claim["evidence"]:

                        st.caption(
                            f"{evidence['segment_id']} "
                            f"(retrieval score: "
                            f"{evidence['score']:.3f})"
                        )
                        st.write(evidence["text"])

                else:
                    st.info(
                        "No supporting evidence was retrieved."
                    )

    else:
        st.info(
            "No verification information is available."
        )

    st.header("📄 Transcripts")


    raw_tab, refined_tab = st.tabs(
        [
            "Raw Transcript",
            "Refined Transcript"
        ]
    )


    with raw_tab:

        st.text_area(
            "Raw transcript",
            result["raw_transcript"],
            height=500
        )


    with refined_tab:

        st.text_area(
            "Refined transcript",
            result["refined_transcript"],
            height=500
        )


    st.header("⬇️ Download Results")


    col1, col2, col3 = st.columns(3)



    with col1:

        st.download_button(
            label="Download Raw Transcript",
            data=result["raw_transcript"],
            file_name="raw_transcript.txt",
            mime="text/plain"
        )



    with col2:

        st.download_button(
            label="Download Refined Transcript",
            data=result["refined_transcript"],
            file_name="refined_transcript.txt",
            mime="text/plain"
        )



    with col3:

        meeting_record_json = json.dumps(
            meeting_record,
            indent=4,
            ensure_ascii=False
        )

        st.download_button(
            label="Download Meeting Record",
            data=meeting_record_json,
            file_name="meeting_record.json",
            mime="application/json"
        )


    if st.session_state.output_dir is not None:

        st.caption(
            f"Results saved to: "
            f"{st.session_state.output_dir}"
        )