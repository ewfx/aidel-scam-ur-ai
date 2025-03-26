
import React, { useState } from 'react';
import FileUploader from './FileUploader';
import TransactionsTable from './TransactionsTable';

const Hero: React.FC = () => {
  const [csvData, setCsvData] = useState<string[][]>([]);
  const [unstructuredData, setUnstructuredData] = useState<string[][]>([]);
  const [showTable, setShowTable] = useState(false);
  const [activeDataType, setActiveDataType] = useState<'structured' | 'unstructured' | null>(null);

  const handleStructuredDataLoaded = (data: string[][]) => {
    setCsvData(data);
    setActiveDataType('structured');
    setShowTable(true);
  };

  const handleUnstructuredDataLoaded = (content: string) => {
    // Parse the unstructured text by splitting on the delimiter "---"
    const sections = content.split('---');
    
    // Create a table-like structure with headers and data
    const headers = ['Transaction Section'];
    const rows = sections.map(section => [section.trim()]);
    
    const tableData = [headers, ...rows];
    setUnstructuredData(tableData);
    setActiveDataType('unstructured');
    setShowTable(true);
  };

  const handleClearData = () => {
    setCsvData([]);
    setUnstructuredData([]);
    setActiveDataType(null);
    setShowTable(false);
  };

  const handleProcessTransactions = () => {
    // This would be where you process the transactions
    if (activeDataType === 'structured') {
      console.log('Processing structured transactions:', csvData);
    } else if (activeDataType === 'unstructured') {
      console.log('Processing unstructured transactions:', unstructuredData);
    }
  };

  return (
    <section className="min-h-screen flex flex-col items-center justify-center px-4 py-20 sm:px-6 lg:px-8 animate-fade-in">
      <div className="max-w-4xl mx-auto text-center space-y-16 w-full">
        <div className="space-y-3">
          
          <h1 className="text-4xl font-bold tracking-tight sm:text-5xl md:text-6xl text-black">
          AI-Driven Entity Intelligence & Risk Analysis
          </h1>
          <span className="inline-block px-3 py-1 text-sm font-medium tracking-wider text-black bg-white border border-black/10 rounded-full shadow-sm">
            Team: scam-ur-ai
          </span>
          <p className="mt-6 text-lg text-black/70">
            Upload transaction files to analyze them for entity risk. Choose between structured and unstructured data formats.
          </p>
        </div>
        
        {showTable ? (
          <TransactionsTable 
            data={activeDataType === 'structured' ? csvData : unstructuredData}
            onClearData={handleClearData}
            onProcessTransactions={handleProcessTransactions}
          />
        ) : (
          <div className="flex flex-col sm:flex-row items-center justify-center gap-6">
            <FileUploader 
              icon="FileText" 
              label="Upload Unstructured Transactions File" 
              acceptedFileTypes=".txt"
              uploadType="unstructured"
              onDataLoaded={handleUnstructuredDataLoaded}
            />
            <FileUploader 
              icon="FileText" 
              label="Upload Structured Transactions File" 
              acceptedFileTypes=".csv"
              uploadType="structured"
              onDataLoaded={handleStructuredDataLoaded}
            />
          </div>
        )}
      </div>
    </section>
  );
};

export default Hero;
