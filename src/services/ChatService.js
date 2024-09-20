export const getChatResponse = async (query) => {
    try {
    //   const response = await fetch('/api/chat', {
    //     method: 'POST',
    //     headers: { 'Content-Type': 'application/json' },
    //     body: JSON.stringify({ query }),
    //   });
    //   const data = await response.json();
      return "demo answer";
    } catch (error) {
      console.error('Error fetching chat response:', error);
      return "Sorry, something went wrong.";
    }
  };
  