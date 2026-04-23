import React from 'react';

function Recommendation({ recommendation }) {
  const parseRecommendation = (text) => {
    const sections = {
      bestPolicy: '',
      comparisonTable: '',
      coverageDetails: '',
      whyExplanation: ''
    };
    
    if (!text) return sections;
    
    const textStr = typeof text === 'string' ? text : JSON.stringify(text);
    
    const bestMatch = textStr.match(/BEST POLICY:(.*?)(?=COMPARISON TABLE:|$)/s);
    if (bestMatch) sections.bestPolicy = bestMatch[1].trim();
    
    const tableMatch = textStr.match(/COMPARISON TABLE:(.*?)(?=COVERAGE DETAILS|$)/s);
    if (tableMatch) sections.comparisonTable = tableMatch[1].trim();
    
    const coverageMatch = textStr.match(/COVERAGE DETAILS:(.*?)(?=WHY THIS POLICY|$)/s);
    if (coverageMatch) sections.coverageDetails = coverageMatch[1].trim();
    
    const whyMatch = textStr.match(/WHY THIS POLICY.*?:(.*?)$/s);
    if (whyMatch) sections.whyExplanation = whyMatch[1].trim();
    
    return sections;
  };
  
  const renderComparisonTable = (tableText) => {
    if (!tableText) return null;
    
    // Split into lines
    const lines = tableText.split('\n');
    
    // Find the separator line (contains |---|)
    let separatorIndex = -1;
    for (let i = 0; i < lines.length; i++) {
      if (lines[i].includes('---') && lines[i].includes('|')) {
        separatorIndex = i;
        break;
      }
    }
    
    // If no separator found, return raw text
    if (separatorIndex === -1) {
      return <pre>{tableText}</pre>;
    }
    
    // Get header line (before separator)
    const headerLine = lines[separatorIndex - 1];
    const headers = headerLine.split('|').filter(cell => cell.trim()).map(cell => cell.trim());
    
    // Get data rows (after separator)
    const dataRows = [];
    for (let i = separatorIndex + 1; i < lines.length; i++) {
      const line = lines[i].trim();
      if (line && line.includes('|') && !line.includes('---')) {
        const cells = line.split('|').filter(cell => cell.trim()).map(cell => cell.trim());
        if (cells.length >= headers.length) {
          dataRows.push(cells);
        }
      }
    }
    
    // Take only first 3 rows to avoid duplicates
    const uniqueRows = [];
    const seenPolicies = new Set();
    for (const row of dataRows) {
      const policyName = row[0];
      if (!seenPolicies.has(policyName)) {
        seenPolicies.add(policyName);
        uniqueRows.push(row);
      }
    }
    const displayRows = uniqueRows.slice(0, 3);
    
    return (
      <div className="table-wrapper">
        <table className="comparison-table">
          <thead>
            <tr>
              {headers.map((header, idx) => (
                <th key={idx}>{header}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {displayRows.map((row, rowIdx) => (
              <tr key={rowIdx}>
                {row.map((cell, cellIdx) => (
                  <td key={cellIdx}>{cell}</td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    );
  };
  
  const renderCoverageDetails = (text) => {
    if (!text) return null;
    
    // Clean up the text - remove markdown formatting
    let cleanText = text
      .replace(/\*\*/g, '')
      .replace(/###/g, '')
      .replace(/^[-\*]\s+/gm, '• ')
      .trim();
    
    return <pre>{cleanText}</pre>;
  };
  
  const parsed = parseRecommendation(recommendation?.recommendation || recommendation);
  
  return (
    <div className="recommendation-container">
      {parsed.bestPolicy && (
        <div className="best-policy-banner">
          <h2>🏆 Best Fit Policy</h2>
          <p>{parsed.bestPolicy}</p>
        </div>
      )}
      
      {parsed.comparisonTable && (
        <div className="comparison-section">
          <h3>📊 Peer Comparison</h3>
          {renderComparisonTable(parsed.comparisonTable)}
        </div>
      )}
      
      {parsed.coverageDetails && (
        <div className="coverage-section">
          <h3>📋 Coverage Details</h3>
          <div className="coverage-content">
            {renderCoverageDetails(parsed.coverageDetails)}
          </div>
        </div>
      )}
      
      {parsed.whyExplanation && (
        <div className="why-section">
          <h3>💡 Why This Policy</h3>
          <div className="why-content">
            <p>{parsed.whyExplanation}</p>
          </div>
        </div>
      )}
    </div>
  );
}

export default Recommendation;