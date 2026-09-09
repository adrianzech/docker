(() => {
  "use strict";

  const calendarText = new Map([
    ["January", "Januar"],
    ["February", "Februar"],
    ["March", "März"],
    ["April", "April"],
    ["May", "Mai"],
    ["June", "Juni"],
    ["July", "Juli"],
    ["August", "August"],
    ["September", "September"],
    ["October", "Oktober"],
    ["November", "November"],
    ["December", "Dezember"],
    ["Mo", "Mo"],
    ["Tu", "Di"],
    ["We", "Mi"],
    ["Th", "Do"],
    ["Fr", "Fr"],
    ["Sa", "Sa"],
    ["Su", "So"],
  ]);

  const weatherText = new Map([
    ["Clear Sky", "Klarer Himmel"],
    ["Mainly Clear", "Überwiegend klar"],
    ["Partly Cloudy", "Teilweise bewölkt"],
    ["Overcast", "Bedeckt"],
    ["Fog", "Nebel"],
    ["Rime Fog", "Reifnebel"],
    ["Drizzle", "Nieselregen"],
    ["Rain", "Regen"],
    ["Moderate Rain", "Mäßiger Regen"],
    ["Heavy Rain", "Starker Regen"],
    ["Freezing Rain", "Gefrierender Regen"],
    ["Snow", "Schnee"],
    ["Moderate Snow", "Mäßiger Schneefall"],
    ["Heavy Snow", "Starker Schneefall"],
    ["Snow Grains", "Schneegriesel"],
    ["Thunderstorm", "Gewitter"],
  ]);

  const exactText = new Map([
    ["Show more", "Mehr anzeigen"],
    ["Show less", "Weniger anzeigen"],
    ["Add task", "Aufgabe hinzufügen"],
    ["Add a task", "Aufgabe hinzufügen"],
    ["No tasks yet.", "Noch keine Aufgaben."],
    ["No tasks to show.", "Keine Aufgaben vorhanden."],
    ["Delete task", "Aufgabe löschen"],
    ["Edit task", "Aufgabe bearbeiten"],
    ["Online", "Erreichbar"],
    ["Offline", "Nicht erreichbar"],
    ["ONLINE", "ERREICHBAR"],
    ["OFFLINE", "NICHT ERREICHBAR"],
    ["No error information provided", "Keine Fehlerinformation verfügbar."],
  ]);

  const exactAttributes = new Map([
    ["Back to current month", "Zurück zum aktuellen Monat"],
    ["Previous month", "Vorheriger Monat"],
    ["Next month", "Nächster Monat"],
    ["Add task", "Aufgabe hinzufügen"],
    ["Add a task", "Aufgabe hinzufügen"],
    ["Delete task", "Aufgabe löschen"],
    ["Edit task", "Aufgabe bearbeiten"],
  ]);

  const boundRefreshButtons = new WeakSet();

  function replaceTextNodes(root, replacements) {
    const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
    let node;
    while ((node = walker.nextNode())) {
      const value = node.nodeValue.trim();
      if (!replacements.has(value)) continue;
      node.nodeValue = node.nodeValue.replace(value, replacements.get(value));
    }
  }

  function localizeCalendar(root) {
    root.querySelectorAll(".widget-type-calendar").forEach((widget) => {
      replaceTextNodes(widget, calendarText);
      widget.querySelectorAll("[title]").forEach((element) => {
        if (exactAttributes.has(element.title)) {
          element.title = exactAttributes.get(element.title);
        }
      });
    });
  }

  function localizeWeather(root) {
    root.querySelectorAll(".widget-type-weather").forEach((widget) => {
      replaceTextNodes(widget, weatherText);
      widget.querySelectorAll(".size-h4.text-center").forEach((element) => {
        element.textContent = element.textContent.replace(/^Feels like\s+/, "Gefühlt ");
      });
      widget.querySelectorAll(".location-icon + div").forEach((element) => {
        element.textContent = element.textContent.replace(/, Austria$/, ", Österreich");
      });
    });
  }

  function localizeRssEmptyState(root) {
    root.querySelectorAll(".widget-type-rss .widget-content li:only-child").forEach((element) => {
      if (element.textContent.trim() !== "No items were returned from the feeds.") return;
      element.textContent = "Keine ungelesenen Artikel.";
      element.classList.add("dashboard-empty-state");
    });
  }

  function localizeInteractiveWidgets(root) {
    root.querySelectorAll(".widget-type-to-do input, .widget-type-to-do textarea, .widget-type-todo input, .widget-type-todo textarea").forEach((element) => {
      if (element.placeholder === "Add a task") element.placeholder = "Aufgabe hinzufügen…";
    });

    root.querySelectorAll(".widget-type-to-do [title], .widget-type-to-do [aria-label], .widget-type-todo [title], .widget-type-todo [aria-label]").forEach((element) => {
      for (const attribute of ["title", "aria-label"]) {
        if (!element.hasAttribute(attribute)) continue;
        const value = element.getAttribute(attribute);
        if (exactAttributes.has(value)) element.setAttribute(attribute, exactAttributes.get(value));
      }
    });
  }

  function setupWidgetRefreshButtons(root) {
    root.querySelectorAll(".dashboard-refreshable .dashboard-widget-refresh").forEach((button) => {
      if (boundRefreshButtons.has(button)) return;
      boundRefreshButtons.add(button);

      button.addEventListener("click", async () => {
        const widget = button.closest(".dashboard-refreshable");
        const widgetId = widget.dataset.widgetId;
        if (!widgetId || typeof window.dynacatRefreshWidget !== "function") return;

        button.disabled = true;
        button.classList.add("is-refreshing");
        button.setAttribute("aria-busy", "true");

        try {
          await window.dynacatRefreshWidget(widgetId);
        } catch (error) {
          console.error("Widget konnte nicht aktualisiert werden:", error);
        } finally {
          button.disabled = false;
          button.classList.remove("is-refreshing");
          button.removeAttribute("aria-busy");
        }
      });
    });
  }

  function localize(root = document) {
    document.documentElement.lang = "de";
    localizeCalendar(root);
    localizeWeather(root);
    localizeRssEmptyState(root);
    localizeInteractiveWidgets(root);
    setupWidgetRefreshButtons(root);
    replaceTextNodes(root, exactText);

    root.querySelectorAll(".widget-error-header .color-negative").forEach((element) => {
      if (element.textContent.trim() === "ERROR") element.textContent = "FEHLER";
    });
  }

  function start() {
    localize();

    let scheduled = false;
    new MutationObserver(() => {
      if (scheduled) return;
      scheduled = true;
      requestAnimationFrame(() => {
        scheduled = false;
        localize();
      });
    }).observe(document.body, { childList: true, subtree: true, characterData: true });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", start, { once: true });
  } else {
    start();
  }
})();
