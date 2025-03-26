
import React, { useRef, useState } from 'react';
import { useToast } from '@/hooks/use-toast';
import UploadButton from './UploadButton';
import { handleFileUpload, parseCSVFile, parseTXTFile } from '@/utils/fileUtils';

interface FileUploaderProps {
  icon: 'FileText' | 'Upload';
  label: string;
  acceptedFileTypes: string;
  uploadType: 'structured' | 'unstructured';
  className?: string;
  onDataLoaded?: ((data: string[][]) => void) | ((content: string) => void);
}

const FileUploader: React.FC<FileUploaderProps> = ({
  icon,
  label,
  acceptedFileTypes,
  uploadType,
  className,
  onDataLoaded,
}) => {
  const { toast } = useToast();
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleUploadClick = () => {
    fileInputRef.current?.click();
  };

  const onFileChange = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    setIsLoading(true);
    
    try {
      await handleFileUpload(file, uploadType);
      
      // For structured (CSV) data, parse and pass to parent
      if (uploadType === 'structured' && onDataLoaded) {
        const parsedData = await parseCSVFile(file);
        (onDataLoaded as (data: string[][]) => void)(parsedData);
      }
      
      // For unstructured (TXT) data, parse and pass to parent
      if (uploadType === 'unstructured' && onDataLoaded) {
        const content = await parseTXTFile(file);
        (onDataLoaded as (content: string) => void)(content);
      }
      
      toast({
        title: "File uploaded successfully",
        description: `Your ${uploadType} file has been uploaded.`,
        variant: "default",
      });
    } catch (error) {
      console.error("Error uploading file:", error);
      toast({
        title: "Upload failed",
        description: "There was an error uploading your file. Please try again.",
        variant: "destructive",
      });
    } finally {
      setIsLoading(false);
      // Reset the file input value so the same file can be uploaded again if needed
      if (fileInputRef.current) {
        fileInputRef.current.value = '';
      }
    }
  };

  return (
    <div className={className}>
      <input
        type="file"
        ref={fileInputRef}
        onChange={onFileChange}
        accept={acceptedFileTypes}
        className="hidden"
        data-testid={`file-input-${uploadType}`}
      />
      <UploadButton
        onClick={handleUploadClick}
        label={label}
        icon={icon}
        isLoading={isLoading}
      />
    </div>
  );
};

export default FileUploader;
