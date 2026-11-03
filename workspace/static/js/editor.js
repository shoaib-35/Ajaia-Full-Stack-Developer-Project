(() => {
    const editorHost = document.getElementById("editor");

    if (!editorHost || !window.Quill) return;

    const editorConfig = window.AJAIA_EDITOR;
    const isEditable = editorConfig.editable;

    const quill = new Quill("#editor", {
        theme: "snow",
        readOnly: !isEditable,
        modules: {
            toolbar: isEditable ? "#toolbar" : false,
        },
    });

    if (!isEditable) return;

    const saveStatus = document.getElementById("save-status");

    let saveTimer = null;
    let activeRequest = null;
    let lastSavedContent = quill.root.innerHTML;

    function setStatus(message, state) {
        saveStatus.textContent = message;
        saveStatus.dataset.state = state || "";
    }

    async function saveDocument() {
        const content = quill.root.innerHTML;

        if (content === lastSavedContent) {
            setStatus("All changes saved", "saved");
            return;
        }

        if (activeRequest) activeRequest.abort();

        activeRequest = new AbortController();
        setStatus("Saving…", "saving");

        try {
            const response = await fetch(editorConfig.saveUrl, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": editorConfig.csrf,
                    "X-Requested-With": "XMLHttpRequest",
                },
                body: JSON.stringify({ content }),
                signal: activeRequest.signal,
            });

            if (!response.ok) {
                throw new Error("Save failed");
            }

            await response.json();
            lastSavedContent = content;
            setStatus("Saved just now", "saved");
        } catch (error) {
            if (error.name !== "AbortError") {
                setStatus(
                    "Unable to save · keep this tab open and retry",
                    "error"
                );
            }
        }
    }

    quill.on("text-change", () => {
        setStatus("Unsaved changes", "pending");
        clearTimeout(saveTimer);
        saveTimer = setTimeout(saveDocument, 750);
    });

    window.addEventListener("beforeunload", (event) => {
        if (quill.root.innerHTML === lastSavedContent) return;

        event.preventDefault();
        event.returnValue = "";
    });

    document.addEventListener("visibilitychange", () => {
        const hasUnsavedChanges =
            quill.root.innerHTML !== lastSavedContent;

        if (document.visibilityState === "hidden" && hasUnsavedChanges) {
            clearTimeout(saveTimer);
            saveDocument();
        }
    });
})();
