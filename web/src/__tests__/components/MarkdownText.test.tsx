import { render, screen } from "@testing-library/react";
import { MarkdownText } from "../../components/MarkdownText";

describe("MarkdownText", () => {
  it("renders heading sections without leaking markdown markers", () => {
    render(
      <MarkdownText
        text={"Here is a quick summary.\n\n### Before You Practice\nRate your confidence"}
      />
    );

    expect(screen.getByText("Here is a quick summary.")).toBeInTheDocument();
    expect(screen.getByText("Before You Practice")).toBeInTheDocument();
    expect(screen.getByText("Rate your confidence")).toBeInTheDocument();
    expect(screen.queryByText("### Before You Practice")).not.toBeInTheDocument();
  });

  it("still supports deeper section headings", () => {
    render(
      <MarkdownText
        text={"#### Quick Tip\nRemember the subject first."}
      />
    );

    expect(screen.getByText("Quick Tip")).toBeInTheDocument();
    expect(screen.getByText("Remember the subject first.")).toBeInTheDocument();
  });
});
