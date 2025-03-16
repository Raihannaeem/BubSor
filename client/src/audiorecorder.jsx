import React, { useState, useRef } from "react";

const AudioRecorder = ({sendToParent}) => {
  const [recording, setRecording] = useState(false);
  const [latestAudio, setLatestAudio] = useState(null);
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);
  const audioRef = useRef(null);

  const toggleRecording = async () => {
    recording ? stopRecording() : await startRecording();
  };

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaRecorderRef.current = new MediaRecorder(stream);
      audioChunksRef.current = []; // Clear previous chunks
      
      mediaRecorderRef.current.ondataavailable = (e) => {
        if (e.data.size > 0) {
          audioChunksRef.current.push(e.data);
        }
      };
      
      mediaRecorderRef.current.onstop = saveRecording;
      mediaRecorderRef.current.start();
      setRecording(true);
    } catch (error) {
      console.error("Error accessing microphone:", error);
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current?.state === "recording") {
      mediaRecorderRef.current.stop();
      setRecording(false);
    }
  };

  const saveRecording = () => {
    if (audioChunksRef.current.length === 0) return; // Prevent empty recordings
    
    const audioBlob = new Blob(audioChunksRef.current, { type: "audio/wav" });
    const file = new File([audioBlob], `recording_${Date.now()}.wav`, { type: "audio/wav" });
    const url = URL.createObjectURL(audioBlob);
    
    // Revoke old URL if it exists
    if (latestAudio) {
      URL.revokeObjectURL(latestAudio.url);
    }
    
    setLatestAudio({ url, file });
    audioChunksRef.current = [];
    
    sendToParent({"file":file,"url":url})

    /*const data = new FormData();
    data.append("file", file);
    fetch("/uploadone", { method: "POST", body: data })
      .then((res) => res.json())
      .then((data) => console.log(data.msg))
      .catch((error) => console.error("Upload error:", error));
    */
    };

  return (
    <div>
      <button onClick={toggleRecording}>{recording? "|" : "."}</button>
    </div>
  );
};

export default AudioRecorder;