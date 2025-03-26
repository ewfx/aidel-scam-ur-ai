/**
 * Process a transaction by sending the data to an API
 * This is a mock implementation that returns random results
 */
export const processTransaction = async (transactionText: string): Promise<any> => {
  // Log the transaction data that would be sent to the API
  console.log('Processing transaction:', { text: transactionText });

  try {
    const response = await fetch('http://127.0.0.1:8000/transaction_analysis', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ text: transactionText })
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error processing transaction:', error);
    throw error;
  }
};
