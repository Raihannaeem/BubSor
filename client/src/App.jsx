import {useState,useEffect,useRef} from 'react';
import AudioRecorder from './audiorecorder';

function App(){
    const [audio,setAudio]=useState('')
    const [output,setOutput]=useState('')
    const [language,setLanguage]=useState('')
    const [audioFile,setAudioFile]=useState(null)
    const [url,setUrl]=useState('')
    const [outputUrl,setOutputUrl]=useState('')

    const inputRef=useRef()
    const fileRef=useRef()
    
    function test(){
        fetch('/members').then((res)=>{
            return res.json()
        }).then((data)=>{
            setOutput(data.data)
        })
    }

    function recieveAudio(data){
        setAudioFile(data.file)
        setUrl(data.url)
        inputRef.current.value=''
    }
    
    function sendMessageTest(){
        const data= new FormData()
        let isFile='n'
        let message=inputRef.current.value

        if(message!=''){
            data.append('type','text')
            data.append('text',message)
            data.append('language','en-IN')
            inputRef.current.value=''
        }
        else if(audioFile!=null){
            data.append('file',audioFile)
            data.append('type','audio')
            data.append('url',url)
            setAudioFile(null)
            setUrl('')
        }
        const file= fileRef.current.files[0]
        if(file!=null){
            data.append('file',file)
            isFile='y'
            fileRef.current.value=''
        }
        data.append('isFile',isFile)
        
        fetch('/fromuser',{
            method:'POST',
            body: data
        }).then((res)=>{
            return res.json()
        }).then((data)=>{
            /*const binary = atob(data.audio_base64)
            const array = new Uint8Array(binary.length)
            for(let i=0; i<binary.length; i++)
                array[i]=binary.charCodeAt(i);

            const audioBlob = new Blob([array], {type: "audio/wav"})
            setOutputUrl(URL.createObjectURL(audioBlob))
            */
            setOutput(data.data)
        })
    }

    return(
        <div>
            <input type='text' ref={inputRef}></input>
            <br/>
            <input type='file' ref={fileRef}/>
            <br/>
            <button onClick={sendMessageTest}>send</button>
            <br/>
            <AudioRecorder sendToParent={recieveAudio}/>
            {url && (
              <div>
                <audio key={url} controls>
                  <source src={url} type="audio/wav" />
                  Your browser does not support the audio element.
                </audio>
              </div>
            )}
            {outputUrl && (
              <div>
                <audio key={outputUrl} controls>
                  <source src={outputUrl} type="audio/wav" />
                  Your browser does not support the audio element.
                </audio>
              </div>
            )}
            <p>{audio}</p>
            {output}
            <p>**whats up**</p>
        </div>
    )
}

export default App