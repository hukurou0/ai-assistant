import React from 'react';
import { auth, GoogleAuthProvider, signInWithPopup } from '../firebaseConfig';

const GoogleAuth: React.FC = () => {
  const handleGoogleLogin = async () => {
    const provider = new GoogleAuthProvider();
    try {
      const result = await signInWithPopup(auth, provider);
      // Googleアカウントからのレスポンスを取得
      const user = result.user;
      console.log("Logged in user:", user);
    } catch (error) {
      console.error("Login Failed:", error);
    }
  };

  return (
    <button onClick={handleGoogleLogin}>Login with Google</button>
  );
};

export default GoogleAuth;
