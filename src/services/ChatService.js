// chatService.js
import { getChatResponse } from '../utils/api'; 
import { normalizeQuery, getAnswerFromKeywords } from '../utils/nlp';
import { faqData } from '../utils/data';

export const handleChatQuery = async (userQuery) => {
  const normalizedQuery = normalizeQuery(userQuery);

  const keywordBasedAnswer = getAnswerFromKeywords(normalizedQuery, faqData);
  if (keywordBasedAnswer) {
    return keywordBasedAnswer;
  }

  // const apiAnswer = await getChatResponse(userQuery);
  const apiAnswer = "call api";
  
  return apiAnswer;
};
