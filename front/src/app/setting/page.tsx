import { getServerSession } from 'next-auth';
import { authOptions } from '@/util/auth';
import { redirect } from 'next/navigation';
import Setting from '@/app/setting/components/Setting';

const Settings = async () => {
  const session = await getServerSession(authOptions);

  if (!session){
    redirect('/');
  }

  return (
    <Setting />
  );
};

export default Settings;
