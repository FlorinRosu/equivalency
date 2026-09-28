import tkinter as tk
from tkinter import ttk


def manualUpdate(equivalencyPairs, notEquivalent):
    """
    Opens a desktop window showing all equivalency pairs as two side-by-side
    lists.

    Right column : the template lecture that has to be equivalenced (read only).
    Left column  : the student lecture currently matched to it, shown as a
                   dropdown (combobox). The dropdown lets the user pick one of
                   the ``notEquivalent`` lectures (promoted lectures that were
                   not automatically matched) for that template lecture.

    Any change made in the UI is written back into ``equivalencyPairs`` and
    ``notEquivalent`` in place, so the caller sees the updated data once the
    window is closed.
    """

    # Nothing to show – keep the previous (silent) behaviour.
    if not equivalencyPairs:
        return

    root = tk.Tk()
    root.title("Manual equivalency check")
    root.geometry("900x600")

    # ------------------------------------------------------------------ #
    # Helper to build a readable label for a lecture.
    # ------------------------------------------------------------------ #
    def lectureLabel(lecture):
        if lecture is None or getattr(lecture, "_name", "") == "":
            return "<empty>"
        grade = getattr(lecture, "_grade", "")
        return f"{lecture._name}  (G={grade})"

    # The pool of lectures the user can choose from for the left column.
    # We keep the actual Lecture objects so we can put them back into the pairs.
    availableLectures = list(notEquivalent)

    # ------------------------------------------------------------------ #
    # Header.
    # ------------------------------------------------------------------ #
    header = tk.Frame(root)
    header.pack(fill="x", padx=10, pady=(10, 0))
    tk.Label(header, text="Student lecture (editable)",
             font=("TkDefaultFont", 10, "bold"), anchor="w").pack(
        side="left", expand=True, fill="x")
    tk.Label(header, text="Template lecture (to be equivalenced)",
             font=("TkDefaultFont", 10, "bold"), anchor="w").pack(
        side="left", expand=True, fill="x")

    # ------------------------------------------------------------------ #
    # Scrollable area that holds one row per equivalency pair.
    # ------------------------------------------------------------------ #
    container = tk.Frame(root)
    container.pack(fill="both", expand=True, padx=10, pady=10)

    canvas = tk.Canvas(container, highlightthickness=0)
    scrollbar = ttk.Scrollbar(container, orient="vertical",
                              command=canvas.yview)
    rowsFrame = tk.Frame(canvas)

    rowsFrame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=rowsFrame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Map each combobox to the pair index it controls and the label -> lecture
    # lookup for its options.
    comboVars = []

    def makeOnSelect(pairIndex, optionMap, combo):
        def onSelect(_event=None):
            selectedLabel = combo.get()
            selectedLecture = optionMap.get(selectedLabel)
            if selectedLecture is None:
                return
            # Assign the chosen student lecture to this template pair.
            equivalencyPairs[pairIndex][0] = selectedLecture
            # Remove it from the not-equivalent pool if it lives there.
            if selectedLecture in notEquivalent:
                notEquivalent.remove(selectedLecture)
        return onSelect

    for index, (studentLecture, templateLecture) in enumerate(equivalencyPairs):
        row = tk.Frame(rowsFrame)
        row.pack(fill="x", pady=2)

        # Build the option list: the current lecture (if any) + the pool.
        optionLectures = []
        if studentLecture is not None and getattr(
                studentLecture, "_name", "") != "":
            optionLectures.append(studentLecture)
        optionLectures.extend(availableLectures)

        optionMap = {lectureLabel(l): l for l in optionLectures}
        # Always allow clearing the selection.
        optionMap["<empty>"] = None
        optionLabels = list(optionMap.keys())

        combo = ttk.Combobox(row, values=optionLabels, state="readonly")
        combo.set(lectureLabel(studentLecture))
        combo.pack(side="left", expand=True, fill="x", padx=(0, 5))
        combo.bind("<<ComboboxSelected>>",
                   makeOnSelect(index, optionMap, combo))
        comboVars.append(combo)

        tk.Label(row, text=lectureLabel(templateLecture),
                 anchor="w").pack(side="left", expand=True, fill="x")

    # ------------------------------------------------------------------ #
    # Bottom bar with a confirm button.
    # ------------------------------------------------------------------ #
    footer = tk.Frame(root)
    footer.pack(fill="x", padx=10, pady=(0, 10))
    tk.Button(footer, text="Done", command=root.destroy).pack(side="right")

    root.mainloop()
