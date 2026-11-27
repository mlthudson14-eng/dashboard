# Megan's Morning Dashboard: setup

Three parts, about 20 minutes in total, done once:

1. Put the page online (free).
2. Build the "Morning Dashboard" Shortcut, which reads Health and your location and opens the page.
3. Add automations that run the Shortcut every morning.

---

## 1. Put the page online with GitHub Pages

This is easiest on a computer, but it also works in Safari on your phone.

1. Create a free account at github.com.
2. Click **+ → New repository**. Name it `dashboard`, set it to **Public**, and tick **Add a README**. Click **Create**.
3. Click **Add file → Upload files** and drop in `index.html`. Click **Commit changes**.
4. Go to **Settings → Pages**. Under *Branch*, choose `main` and `/ (root)`, then **Save**.
5. After about a minute, your page is live at:
   `https://mlthudson14-eng.github.io/dashboard/`

Open that link on your phone once to check that it loads. It will show sample numbers until the Shortcut runs.

**Privacy:** the page file is public, but it contains nothing personal except your first name. Your Health numbers go after a `#` in the link, and browsers never send that part to the server. They stay on your phone. Weather is looked up from Open-Meteo using your location rounded to about 1 km.

---

## 2. Build the Shortcut

In the **Shortcuts** app, tap **+** and name the shortcut **Morning Dashboard**. Add these actions in order. Wherever a step says **Set Variable** `Name`, add a *Set Variable* action and type that name. Later steps pick it from the variable list. Action names can differ slightly between iOS versions.

### Sleep
1. **Date** → tap the date and type `yesterday 6:00 PM`.
   **Set Variable** `SleepWindow`
2. **Find Health Samples**
   - Type: **Sleep** (called *Sleep Analysis* on older iOS versions)
   - Filter: *Start Date* **is in the last** `2` **days**
   - Filter: *Value* **is not** In Bed
   - Filter: *Value* **is not** Awake
   - *(If you wear an Apple Watch, also add: Source **is** your watch. This stops iPhone and Watch sleep from being counted twice.)*
   - Sort by **Start Date**, **Oldest First**
3. **Repeat with Each** (it uses the Health Samples automatically). Inside it, add:
   - **If**: tap *Input* → choose **Repeat Item**, tap it again and pick **Start Date**. Condition: **is after**. Value: tap and choose the `SleepWindow` variable.
     - Inside the If: **Add to Variable**: `Repeat Item` → variable name `Night`
   - Leave *Otherwise* empty, then **End If**.
4. **End Repeat**
5. **Repeat with Each** item in `Night`:
   - **Get Time Between Dates**: tap the first date → Repeat Item → **Start Date**, then the second → Repeat Item → **End Date**. Unit: **Minutes**.
6. **End Repeat** → **Calculate Statistics**: **Sum** of *Repeat Results* → **Round Number** (Ones) → **Set Variable** `Sleep`
7. **Get Item from List**: **First Item** of `Night` → **Get Details of Health Sample**: Start Date → **Format Date**: Custom, `HH:mm` → **Set Variable** `Bed`
8. **Get Item from List**: **Last Item** of `Night` → **Get Details of Health Sample**: End Date → **Format Date**: Custom, `HH:mm` → **Set Variable** `Wake`

The two-day search catches everything. The **If** then keeps only the sleep that started after 6 PM yesterday. If you ever go to bed before 6 PM, change step 1 to `yesterday 4:00 PM`.

### Yesterday's activity
9. **Find Health Samples**
   - Type: **Steps**
   - Filter: *Start Date* **is in the last** `1` **days**
   - Filter: *Start Date* **is not today**
   - → **Calculate Statistics**: **Sum** → **Round Number** (Ones) → **Set Variable** `Steps`
10. Same as step 9 with Type **Active Energy** → **Set Variable** `Cal`
11. Same as step 9 with Type **Exercise Minutes** (sometimes listed as *Apple Exercise Time*) → **Set Variable** `Ex`

These two filters together mean "yesterday", without needing date variables.

### Recovery
12. **Find Health Samples**: Type **Heart Rate Variability**, sort by Start Date **Latest First**, **Limit 1** → **Get Details**: Value → **Round Number** → **Set Variable** `HRV`
13. **Find Health Samples**: Type **Resting Heart Rate**, sort **Latest First**, **Limit 1** → **Get Details**: Value → **Round Number** → **Set Variable** `RHR`

### Location (for weather)
14. **Get Current Location** → **Get Details of Locations**: Latitude → **Round Number** (Hundredths) → **Set Variable** `Lat`
15. **Get Current Location** → **Get Details of Locations**: Longitude → **Round Number** (Hundredths) → **Set Variable** `Lon`

### Open the dashboard
16. **Text**: type the link below, all on one line with no spaces. Wherever it shows `[Name]`, delete that and insert the variable with that name from the bar above the keyboard.

```
https://mlthudson14-eng.github.io/dashboard/#sleep=[Sleep]&bed=[Bed]&wake=[Wake]&steps=[Steps]&cal=[Cal]&ex=[Ex]&rhr=[RHR]&hrv=[HRV]&lat=[Lat]&lon=[Lon]
```

17. **Open URLs** (Text)

Tap ▶ to run it. The first time, iOS asks for permission to read each Health type and your location. Tap **Allow**. The dashboard should open in Safari with your real numbers.

Tip: if a value shows as blank or `–`, run the shortcut with a **Show Result** action after that step to see what it produced.

---

## 3. Run it automatically every morning

iPhones can't run anything "on unlock". The closest equivalent is to run the Shortcut at wake-up, so the dashboard is already open in Safari when you unlock.

**Option A (recommended): when your alarm stops**
Shortcuts → **Automation** → **+** → **Alarm** → **Is Stopped** (any alarm) → **Run Immediately** → action **Run Shortcut: Morning Dashboard**.
This follows your 5:00 AM weekday and 7:00 AM weekend alarms automatically.

**Option B: fixed times**
Make two **Time of Day** automations, both set to **Run Immediately**:
- **5:00 AM**, repeat **Weekdays** → Run Shortcut: Morning Dashboard
- **7:00 AM**, repeat **Weekends** → Run Shortcut: Morning Dashboard

---

## Using the dashboard

- **Settings (gear icon):** change your name, habits (one per line, up to 6), sleep goal, step goal and °F/°C.
- **Habits** reset every morning. The streak counts consecutive days you ticked them off.
- **Tasks:** unfinished tasks carry over to the next day. Finished ones clear overnight. Tap **×** to delete one.
- **Recovery** compares this morning's HRV and resting heart rate with your own average. That starts after 5 mornings of data.
- **The 7-night strip** next to last night's sleep fills in as the days go by. Dark bars are nights you met your goal.

**Important:** keep using the dashboard in **Safari**, the app the Shortcut opens. Habits, tasks and history are saved in Safari's storage on your phone. A home-screen web app would have separate, empty storage. Clearing Safari's website data also clears them.
