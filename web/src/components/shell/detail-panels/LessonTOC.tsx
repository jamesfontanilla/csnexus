/**
 * Lesson Table of Contents — detail panel stub.
 * Renders when viewing a lesson at /subtopics/:subtopicId/lesson.
 * Will eventually display the actual lesson structure fetched from lesson data.
 */
export default function LessonTOC() {
  return (
    <div className="detail-panel-content" data-testid="lesson-toc">
      <h3 className="detail-panel-content__heading">Table of Contents</h3>
      <ol className="detail-panel-content__list">
        <li className="detail-panel-content__item detail-panel-content__item--active">
          Introduction
        </li>
        <li className="detail-panel-content__item">Key Concepts</li>
        <li className="detail-panel-content__item">Examples</li>
        <li className="detail-panel-content__item">Practice Problems</li>
        <li className="detail-panel-content__item">Summary</li>
      </ol>
    </div>
  );
}
