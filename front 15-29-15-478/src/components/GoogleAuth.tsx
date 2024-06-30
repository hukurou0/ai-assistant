import React from 'react';
import { auth, GoogleAuthProvider, signInWithPopup } from '../firebaseConfig';

const GoogleAuth: React.FC = () => {
  const handleGoogleLogin = async () => {
    const provider = new GoogleAuthProvider();
    try {
      const result = await signInWithPopup(auth, provider);
      // Googleアカウントからのレスポンスを取得
      const user = result.user;

      if (user) {
        // ユーザーがログインしている場合、IDトークンを取得
        user.getIdToken().then((idToken) => {
          console.log("Firebase ID Token:", idToken);
        }).catch((error) => {
          console.error("Error getting ID Token:", error);
        });
      }
    } catch (error) {
      console.error("Login Failed:", error);
    }
  };

  return (
    <button onClick={handleGoogleLogin}>Login with Google</button>
  );
};

export default GoogleAuth;
