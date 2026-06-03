/**
 * Tutor Context — detail panel stub.
 * Renders when viewing the tutor at /tutor.
 * Will eventually display chat context: lesson references, topic outline,
 * and relevant learning materials for the current conversation.
 */
export default function TutorContext() {
  return (
    <div className="detail-panel-content" data-testid="tutor-context">
      <h3 className="detail-panel-content__heading">Context</h3>
      <section className="detail-panel-content__section">
        <h4 className="detail-panel-content__subheading">Lesson References</h4>
        <ul className="detail-panel-content__list">
          <li className="detail-panel-content__item">No references yet</li>
        </ul>
      </section>
      <section className="detail-panel-content__section">
        <h4 className="detail-panel-content__subheading">Topic Outline</h4>
        <ul className="detail-panel-content__list">
          <li className="detail-panel-content__item">Start a conversation to see context</li>
        </ul>
      </section>
    </div>
  );
}
