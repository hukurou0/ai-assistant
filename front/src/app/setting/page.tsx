import { getServerSession } from 'next-auth';
import { authOptions } from '@/util/auth';
import { redirect } from 'next/navigation';
import Setting from '@/components/Setting';
import Box from '@/components/Box';
import Login from '@/components/Login';

const Settings = async () => {
  const session = await getServerSession(authOptions);

  if (!session){
    redirect('/');
  }

  return (
    <>
      {session?.error === 'RefreshTokenExpiredError' || !session ? (
        <Box>
          <Login />
        </Box>
      ) : (
        <Setting />
      )}
    </>
  );
};

export default Settings;
