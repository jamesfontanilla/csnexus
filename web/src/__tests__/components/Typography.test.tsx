import { describe, it, expect } from "vitest";
import { render } from "@testing-library/react";
import { Body, Caption, Code } from "../../components/Typography";

describe("Typography", () => {
  describe("Body", () => {
    it("renders with max-width: 680px", () => {
      const { container } = render(<Body>Some body text</Body>);
      const el = container.querySelector("p")!;
      expect(el.style.maxWidth).toBe("680px");
    });
  });

  describe("Caption", () => {
    it("uses --color-text-secondary for color", () => {
      const { container } = render(<Caption>A caption</Caption>);
      const el = container.querySelector("span")!;
      expect(el.style.color).toBe("var(--color-text-secondary)");
    });
  });

  describe("Code", () => {
    it("renders a <code> element with padding '0 var(--space-2)' when inline", () => {
      const { container } = render(<Code inline>const x = 1;</Code>);
      const codeEl = container.querySelector("code")!;
      expect(codeEl).toBeTruthy();
      expect(codeEl.style.padding).toBe("0 var(--space-2)");
    });

    it("renders a <pre> element with padding 'var(--space-4)' when inline={false}", () => {
      const { container } = render(
        <Code inline={false}>{"function hello() {}"}</Code>
      );
      const preEl = container.querySelector("pre")!;
      expect(preEl).toBeTruthy();
      expect(preEl.style.padding).toBe("var(--space-4)");
    });
  });
});
