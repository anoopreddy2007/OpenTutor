export const concepts = [
  { name:'Variables & Data Types', mastery:92, status:'mastered', tone:'success' },
  { name:'Control Flow', mastery:84, status:'stable', tone:'success' },
  { name:'Functions', mastery:48, status:'frontier', tone:'primary' },
  { name:'Recursion', mastery:31, status:'attention', tone:'warning' },
  { name:'Object-Oriented Programming', mastery:18, status:'locked', tone:'muted' },
]

export const recommendations = [
  { title:'Practice Functions', action:'PRACTICE_CONCEPT', reason:'Mastery is low and additional practice is needed.', mastery:48, confidence:35, icon:'target' },
  { title:'Review Recursion prerequisites', action:'REVIEW_PREREQUISITES', reason:'A prerequisite gap is limiting progress on this concept.', mastery:31, confidence:28, icon:'git' },
  { title:'Revisit Control Flow', action:'REVIEW_CONCEPT', reason:'Retrieval is due and a short review will reinforce retention.', mastery:84, confidence:71, icon:'refresh' },
]

export const history = [
  { date:'Today', items:[['Completed Functions assessment','8 / 10','success'],['Practiced Variables','Mastery updated','success'],['Tutor session','Recursion','info']] },
  { date:'Yesterday', items:[['Reviewed Data Types','12 min','success'],['Practice session','Control Flow','info']] },
]
