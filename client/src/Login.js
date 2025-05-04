import React, { useState } from 'react';

export default function Login(){


        const [firstname, setFirstname] = useState("");
        const [password, setPassword] = useState("");
        const [Email, setEmail] = useState("");
        const [VerificationP, setVerificationP] = useState("");

    
        const handleChange = (event) => {
            const { name, value } = event.target;
            if (name === "firstname") setFirstname(value);
            if (name === "password") setPassword(value);
            if (name === "Email") setEmail(value);
            if (name === "VerificationP") setVerificationP(value);
        };
  

    const handleSubmit = async (event) => {
        event.preventDefault();

        const userData = { firstname: firstname, password: password};
     
        try {
           const response = await fetch("http://127.0.0.1:5000/Login", {
           method: "POST",  
           headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(userData),  
      });

       const data = await response.json(); 
       if (response.ok) {
         alert("התחברת בהצלחה");
       } else {
         alert(data.error || "לא ניתן להתחבר");
       }
     } catch (error) {
       alert("התרחשה שגיאה, נסה שנית");
     }
    };
    
   
  return (
     <div>
         <h1>
          welcome to fit me!!
            <br></br>
            התחברות
           <br></br>
          </h1>
          <input type="text" name="firstname" placeholder="שם משתמש" value={firstname}
          onChange={handleChange} ></input> <br></br>
          <input type="password" name="password" placeholder="סיסמא " value={password}
          onChange={handleChange} ></input> <br></br>
          <button onClick={handleSubmit}>התחבר</button>             
             {/* <p>
                שכחתי סיסמא
                <br></br>
                <br></br>
                <input type="text" name="Email" placeholder="הכנס כתובת מייל " value={Email}
                onChange={handleChange} ></input> <br></br>
                <input type="text" name="VerificationP" placeholder="אימות סיסמא " value={VerificationP}
                onChange={handleChange} ></input>
                <button>שלח</button>
            </p>
    //  */}
       </div>
        
    )
 };
