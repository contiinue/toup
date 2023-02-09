import '../../css/auth.css'
import { useState } from 'react';
import { redirect } from "react-router-dom";
import { useNavigate } from "react-router-dom";
import {parseJwt, setCookie} from './../utils/cookies'

// function parseJwt (token) {
//     var base64Url = token.split('.')[1];
//     var base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
//     var jsonPayload = decodeURIComponent(window.atob(base64).split('').map(function(c) {
//         return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
//     }).join(''));

//     return JSON.parse(jsonPayload);
// }


// function getCookie(name) {
//     const value = `; ${document.cookie}`;
//     const parts = value.split(`; ${name}=`);
//     if (parts.length === 2) return parts.pop().split(';').shift();
//   }



// function setCookie(name,value,days) {
//     var expires = "";
//     if (days) {
//         var date = new Date();
//         date.setTime(date.getTime() + (days*24*60*60*1000));
//         expires = "; expires=" + date.toUTCString();
//     }
//     document.cookie = name + "=" + (value || "")  + expires + "; path=/";
// }


async function requestAuth(login, password, is_remember) {

    let response = await fetch(
        'http://127.0.0.1:8000/api/v1/token/', {
        method: 'POST',
        body: JSON.stringify({'username': login, 'password': password}),
        headers: {
            'Content-Type': 'application/json'
          },
      
    })
    let data = await response.json()
    setCookie('access', data.access)
    setCookie('refresh', data.refresh)
    return `/profile/${parseJwt(data.access).username}`
}


export default function Login(props) {
    const [login, setlogin] = useState("");
    const [password, setPassword] = useState("");
    const [remember, SetRemember] = useState('')
    const navigate = useNavigate();

    return (
        <div className="container">
            <label for="uname"><b>Username</b></label>
            <input type="text" value={login} onChange={(e) => {setlogin(e.target.value)}} placeholder="Enter Username" name="uname" required/>
        
            <label for="psw"><b>Password</b></label>
            <input type="password" value={password} onChange={(e) => {setPassword(e.target.value)}} placeholder="Enter Password" name="psw" required/>
                
            <button type="submit" onClick={async (e) => {navigate(await requestAuth(login, password, remember))}}>Login</button>
            <label>
            <input type="checkbox" value={remember} onChange={(e) => {SetRemember(e.target.value)}} checked="checked" name="remember"/> Remember me
            </label>
        </div>
    )
}