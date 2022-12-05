import React, {useEffect, useState} from "react";
import httpClient from "../httpClient";


const LoginPage: React.FC = () => {

    const [email, setEmail] = useState <string>(""); 
    const [password, setPassword] = useState <string>(""); 

    const logInUser = async () => {
        console.log(email, password);
    
        try {
          const resp = await httpClient.post("http://127.0.0.1:5000/login", {
            email,
            password,
          });
    
          window.location.href = "/";
        } catch (error: any) {
          if (error.response.status === 401) {
            alert("Invalid credentials");
          }
        }
      };

  
    return (
    <div>
        <h1>Login to your account</h1>
        <form>
            <label>Email:</label>
            <input type="text" value={email} onChange={(e) => setEmail(e.target.value)} id=""/>
            <label>Passowrd:</label>
             <input type="text" value={password} onChange={(e) => setPassword(e.target.value)} id=""/>

             <button type="button" onClick={() => logInUser()}>Submit</button>
        </form>
        
        </div>
        
        
      
    );
  };
  
  export default LoginPage;