import { FC, ReactNode } from 'react';

interface BoxProps {
  children: ReactNode;
  className?: string;
}

const Box: FC<BoxProps> = ({ children, className = '' }) => {
  return (
    <div className={`p-4 ${className}`}>
      {children}
    </div>
  );
};

export default Box;