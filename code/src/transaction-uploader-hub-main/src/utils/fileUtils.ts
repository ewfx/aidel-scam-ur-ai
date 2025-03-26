
/**
 * Handles the file upload process based on file type
 */
export const handleFileUpload = async (file: File, type: 'structured' | 'unstructured'): Promise<void> => {
  // This is a simulation of file processing
  // In a real application, you would send this file to your server
  return new Promise((resolve, reject) => {
    // Validating file type
    if (type === 'structured' && !file.name.endsWith('.csv')) {
      reject(new Error('Only CSV files are accepted for structured data'));
      return;
    }
    
    if (type === 'unstructured' && !file.name.endsWith('.txt')) {
      reject(new Error('Only TXT files are accepted for unstructured data'));
      return;
    }
    
    // Simulating server processing time
    setTimeout(() => {
      console.log(`Processing ${type} file:`, file.name);
      
      // Here you would typically upload the file to a server
      // For now, we'll just resolve the promise
      resolve();
    }, 1500);
  });
};

/**
 * Parses a CSV file and returns the data
 */
export const parseCSVFile = (file: File): Promise<string[][]> => {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    
    reader.onload = (event) => {
      try {
        const csv = event.target?.result as string;
        const lines = csv.split('\n');
        const result = lines.map(line => line.split(','));
        resolve(result);
      } catch (error) {
        reject(error);
      }
    };
    
    reader.onerror = (error) => reject(error);
    
    reader.readAsText(file);
  });
};

/**
 * Parses a TXT file and returns the content
 */
export const parseTXTFile = (file: File): Promise<string> => {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    
    reader.onload = (event) => {
      try {
        const content = event.target?.result as string;
        resolve(content);
      } catch (error) {
        reject(error);
      }
    };
    
    reader.onerror = (error) => reject(error);
    
    reader.readAsText(file);
  });
};
