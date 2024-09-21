import { synonyms } from './data';

export const normalizeQuery = (query) => {
  let normalizedQuery = query.toLowerCase();

  for (let key in synonyms) {
    synonyms[key].forEach(synonym => {
      const regex = new RegExp(`\\b${synonym}\\b`, 'g');
      normalizedQuery = normalizedQuery.replace(regex, key);
    });
  }

  return normalizedQuery;
};

export const levenshteinDistance = (a, b) => {
  const matrix = [];

  for (let i = 0; i <= b.length; i++) {
    matrix[i] = [i];
  }

  for (let j = 0; j <= a.length; j++) {
    matrix[0][j] = j;
  }

  for (let i = 1; i <= b.length; i++) {
    for (let j = 1; j <= a.length; j++) {
      if (b.charAt(i - 1) === a.charAt(j - 1)) {
        matrix[i][j] = matrix[i - 1][j - 1];
      } else {
        matrix[i][j] = Math.min(matrix[i - 1][j - 1] + 1,
                                matrix[i][j - 1] + 1,
                                matrix[i - 1][j] + 1);
      }
    }
  }

  return matrix[b.length][a.length];
};

export const getAnswerFromKeywords = (query, faqData, threshold = 3) => {
  const normalizedQuery = normalizeQuery(query);

  let bestMatch = null;
  let minDistance = Infinity;
  
  faqData.forEach(faq => {
    const distance = levenshteinDistance(normalizedQuery, faq.keyword);
    if (distance < minDistance) {
      minDistance = distance;
      bestMatch = faq;
    }
  });

  // Return the answer only if the minimum distance is within the threshold
  return minDistance <= threshold ? bestMatch.answer : null;
};
