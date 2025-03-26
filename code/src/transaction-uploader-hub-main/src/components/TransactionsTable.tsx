import React, { useState } from 'react';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { Button } from '@/components/ui/button';
import { Plus, Download, Loader } from 'lucide-react';
import { processTransaction } from '@/utils/apiUtils';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog';

interface TransactionsTableProps {
  data: string[][];
  onClearData: () => void;
  onProcessTransactions: () => void;
}

const TransactionsTable: React.FC<TransactionsTableProps> = ({
  data,
  onClearData,
  onProcessTransactions,
}) => {
  // Get headers from the first row of the CSV data
  const headers = data[0] || [];
  // Get rows from the rest of the CSV data
  const rows = data.slice(1);
  // Track which rows have been processed and have results
  const [processedRows, setProcessedRows] = useState<Record<number, any>>({});
  // Track if all rows have been processed
  const [allProcessed, setAllProcessed] = useState(false);
  // State for dialog
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [selectedResult, setSelectedResult] = useState<any>(null);
  // Track loading state for each row
  const [loadingRows, setLoadingRows] = useState<Record<number, boolean>>({});

  // Process all transactions one by one
  const handleProcessAllTransactions = async () => {
    onProcessTransactions();
    
    // Process each row sequentially
    for (let i = 0; i < rows.length; i++) {
      const row = rows[i];
      setLoadingRows(prev => ({ ...prev, [i]: true }));
      const result = await processRowData(row, headers);
      setLoadingRows(prev => ({ ...prev, [i]: false }));
      
      // Update processed rows with the result
      setProcessedRows(prev => ({
        ...prev,
        [i]: result
      }));
    }
    
    // Set allProcessed to true after all rows have been processed
    setAllProcessed(true);
  };

  // Process individual row data
  const processRowData = async (row: string[], headers: string[]) => {
    // For structured data (CSV), create a JSON object from column names and values
    if (headers.length > 1) {
      const rowData: Record<string, string> = {};
      headers.forEach((header, index) => {
        if (index < row.length) {
          rowData[header] = row[index];
        }
      });
      
      // Convert to multi-line text
      const formattedText = Object.entries(rowData)
        .map(([key, value]) => `${key}: ${value}`)
        .join('\n');
      
      return await processTransaction(formattedText);
    } 
    // For unstructured data (TXT), use the single column text directly
    else if (row.length > 0) {
      return await processTransaction(row[0]);
    }
    
    return null;
  };

  // View the processed result for a specific row
  const handleViewResult = (rowIndex: number) => {
    const result = processedRows[rowIndex];
    if (result) {
      setSelectedResult(result);
      setIsDialogOpen(true);
    }
  };

  // Download processed data as JSON
  const handleDownloadJSON = () => {
    // Collect all processed results into an array
    const resultsArray = Object.values(processedRows);
    
    // Create a JSON string from the results array
    const jsonString = JSON.stringify(resultsArray, null, 2);
    
    // Create a Blob from the JSON string
    const blob = new Blob([jsonString], { type: 'application/json' });
    
    // Create a download link and trigger the download
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = 'transactions.json';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  };

  // Download processed data as CSV
  const handleDownloadCSV = () => {
    // If there are no processed rows, return
    if (Object.keys(processedRows).length === 0) return;
    
    // Get all unique keys from all result objects
    const allKeys = new Set<string>();
    Object.values(processedRows).forEach(result => {
      Object.keys(result).forEach(key => {
        allKeys.add(key);
      });
    });
    
    // Convert Set to Array for easier handling
    const csvHeaders = Array.from(allKeys);
    
    // Create CSV header row
    let csvContent = csvHeaders.join(',') + '\n';
    
    // Create CSV data rows
    Object.values(processedRows).forEach(result => {
      const rowValues = csvHeaders.map(header => {
        // Handle nested arrays by joining them with semicolons
        if (Array.isArray(result[header])) {
          return `"${result[header].join(';')}"`;
        }
        // Handle undefined values
        if (result[header] === undefined) {
          return '';
        }
        // Handle string values that might contain commas
        if (typeof result[header] === 'string' && result[header].includes(',')) {
          return `"${result[header]}"`;
        }
        return result[header];
      });
      csvContent += rowValues.join(',') + '\n';
    });
    
    // Create a Blob from the CSV content
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    
    // Create a download link and trigger the download
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = 'transactions.csv';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  };

  return (
    <div className="space-y-6 w-full max-w-4xl mx-auto">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-xl font-bold">Transaction Data</h2>
        <div className="flex gap-4">
          <Button
            onClick={handleProcessAllTransactions}
            className="bg-black text-white hover:bg-black/80"
          >
            Process Transactions
          </Button>
          <Button
            onClick={onClearData}
            variant="outline"
            className="border-black text-black hover:bg-black/10"
          >
            Clear Data
          </Button>
        </div>
      </div>

      <div className="rounded-md border overflow-hidden">
        <Table>
          <TableHeader>
            <TableRow>
              {headers.map((header, index) => (
                <TableHead key={index} className='text-center'>{header}</TableHead>
              ))}
              <TableHead>View Results</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {rows.map((row, rowIndex) => (
              <TableRow key={rowIndex}>
                {row.map((cell, cellIndex) => (
                  <TableCell key={cellIndex}>{cell}</TableCell>
                ))}
                <TableCell>
                  <div className="flex items-center justify-center">
                    <Button 
                      size="icon" 
                      variant="default" 
                      disabled={!processedRows[rowIndex]} 
                      className="h-8 w-8"
                      onClick={() => handleViewResult(rowIndex)}
                    >
                      <Plus className="h-4 w-4" />
                    </Button>
                    {loadingRows[rowIndex] && <Loader className="ml-2 animate-spin h-4 w-4" />}
                  </div>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>
      
      {/* Download buttons - shown only after all rows have been processed */}
      {allProcessed && (
        <div className="flex justify-end gap-4 mt-6">
          <Button
            onClick={handleDownloadJSON}
            variant="outline"
            className="border-black text-black hover:bg-black/10 flex items-center gap-2"
          >
            <Download className="h-4 w-4" />
            Download as JSON
          </Button>
          <Button
            onClick={handleDownloadCSV}
            variant="outline"
            className="border-black text-black hover:bg-black/10 flex items-center gap-2"
          >
            <Download className="h-4 w-4" />
            Download as CSV
          </Button>
        </div>
      )}

      {/* Dialog for displaying result details */}
      <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
        <DialogContent className="max-w-lg max-h-[80vh] overflow-y-auto">
          <DialogHeader>
            <DialogTitle>Transaction Results</DialogTitle>
          </DialogHeader>
          <div className="mt-4 p-4 bg-gray-100 rounded-md overflow-x-auto">
            <pre className="text-sm whitespace-pre-wrap break-all">
              {selectedResult && JSON.stringify(selectedResult, null, 2)}
            </pre>
          </div>
        </DialogContent>
      </Dialog>
    </div>
  );
};

export default TransactionsTable;
