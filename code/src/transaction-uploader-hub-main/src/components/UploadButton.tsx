
import React from 'react';
import { Button } from '@/components/ui/button';
import { cn } from '@/lib/utils';
import * as LucideIcons from 'lucide-react';

// Define the icon names we'll use in our application
type IconName = 'FileText' | 'Upload' | 'Loader2';

interface UploadButtonProps {
  onClick: () => void;
  label: string;
  icon: IconName;
  isLoading?: boolean;
  className?: string;
}

const UploadButton: React.FC<UploadButtonProps> = ({
  onClick,
  label,
  icon,
  isLoading = false,
  className,
}) => {
  // Get the icon component from Lucide
  const IconComponent = LucideIcons[icon];

  return (
    <Button
      onClick={onClick}
      className={cn(
        "group relative flex items-center gap-2 px-6 py-6 bg-black text-white border-none rounded-xl transition-all duration-300 overflow-hidden button-hover-effect",
        className
      )}
      disabled={isLoading}
    >
      {isLoading ? (
        <LucideIcons.Loader2 className="h-4 w-4 mr-2 animate-spin" />
      ) : (
        <IconComponent className="h-4 w-4 mr-2 transition-transform duration-300 group-hover:scale-110" />
      )}
      <span className="font-medium">{label}</span>
    </Button>
  );
};

export default UploadButton;
