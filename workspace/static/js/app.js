(() => {
    // Modal open and close controls.
    document.querySelectorAll("[data-open-modal]").forEach((button) => {
        button.addEventListener("click", () => {
            const modal = document.getElementById(button.dataset.openModal);
            if (!modal) return;

            modal.classList.add("open");
            modal.setAttribute("aria-hidden", "false");

            const firstFocusable = modal.querySelector("button, input");
            if (firstFocusable) firstFocusable.focus();
        });
    });

    document.querySelectorAll("[data-close-modal]").forEach((button) => {
        button.addEventListener("click", () => {
            const modal = button.closest(".modal-backdrop");
            if (!modal) return;

            modal.classList.remove("open");
            modal.setAttribute("aria-hidden", "true");
        });
    });

    document.querySelectorAll(".modal-backdrop").forEach((modal) => {
        modal.addEventListener("click", (event) => {
            if (event.target !== modal) return;

            modal.classList.remove("open");
            modal.setAttribute("aria-hidden", "true");
        });
    });

    document.addEventListener("keydown", (event) => {
        if (event.key !== "Escape") return;

        document.querySelectorAll(".modal-backdrop.open").forEach((modal) => {
            modal.classList.remove("open");
            modal.setAttribute("aria-hidden", "true");
        });
    });

    // Show or hide password fields.
    document.querySelectorAll("[data-password-target]").forEach((button) => {
        button.addEventListener("click", () => {
            const input = document.getElementById(
                button.dataset.passwordTarget
            );
            if (!input) return;

            const isVisible = input.type === "password";
            input.type = isVisible ? "text" : "password";
            button.textContent = isVisible ? "Hide" : "Show";
            button.setAttribute(
                "aria-label",
                isVisible ? "Hide password" : "Show password"
            );
        });
    });

    // Confirm destructive form submissions.
    document.querySelectorAll("[data-confirm]").forEach((form) => {
        form.addEventListener("submit", (event) => {
            if (!window.confirm(form.dataset.confirm)) {
                event.preventDefault();
            }
        });
    });

    // Dismiss Django message notifications.
    document.querySelectorAll(".message-close").forEach((button) => {
        button.addEventListener("click", () => {
            button.parentElement.remove();
        });
    });

    // Responsive sidebar and persisted desktop collapse state.
    const menuToggle = document.getElementById("menu-toggle");
    const sidebar = document.getElementById("sidebar");
    const sidebarCollapse = document.getElementById("sidebar-collapse");

    if (menuToggle && sidebar) {
        menuToggle.addEventListener("click", () => {
            sidebar.classList.toggle("open");
        });
    }

    if (sidebarCollapse && sidebar) {
        const storageKey = "ajaia-sidebar-collapsed";

        if (localStorage.getItem(storageKey) === "1") {
            document.body.classList.add("sidebar-collapsed");
        }

        const updateCollapseControl = () => {
            const isCollapsed = document.body.classList.contains(
                "sidebar-collapsed"
            );

            sidebarCollapse.setAttribute(
                "aria-expanded",
                String(!isCollapsed)
            );
            sidebarCollapse.setAttribute(
                "aria-label",
                isCollapsed ? "Expand sidebar" : "Collapse sidebar"
            );
            sidebarCollapse.title = isCollapsed
                ? "Expand sidebar"
                : "Collapse sidebar";
            sidebarCollapse.textContent = isCollapsed ? "›" : "‹";
        };

        updateCollapseControl();

        sidebarCollapse.addEventListener("click", () => {
            document.body.classList.toggle("sidebar-collapsed");

            const isCollapsed = document.body.classList.contains(
                "sidebar-collapsed"
            );
            localStorage.setItem(storageKey, isCollapsed ? "1" : "0");
            updateCollapseControl();
        });
    }

    // Display the selected upload's filename.
    const fileInput = document.getElementById("file-input");
    const fileName = document.getElementById("file-name");

    if (fileInput && fileName) {
        fileInput.addEventListener("change", () => {
            fileName.textContent = fileInput.files.length
                ? fileInput.files[0].name
                : "No file selected";
        });
    }
})();
