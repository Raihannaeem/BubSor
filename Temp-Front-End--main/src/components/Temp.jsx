import {useState,useRef} from 'react'

function Temp(){
    const [sample,setSample]=useState('')

    function getdata(){
        fetch('/members').then((res)=>{
            return res.json()
        }).then((data)=>{
            setSample(data.data)
        })
    }

    return(
        <div>
            <p>{sample}</p>
            <button onClick={getdata}>click me</button>
        </div>
    )
}

export default Temp