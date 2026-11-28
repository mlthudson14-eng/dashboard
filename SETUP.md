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
1. **Find Health Samples**
   - Type: **Sleep** (called *Sleep Analysis* on older iOS versions)
   - Filter: *Start Date* **is in the last** `2` **days**
   - Filter: *Value* **is not** In Bed
   - Filter: *Value* **is not** Awake
   - **All** filters must be true. No source filter, no limit.
   - Sort by **Start Date**, **Oldest First**
2. **Repeat with Each** (it uses the Health Samples automatically). Inside it, add:
   - **Format Date**: Repeat Item → **Start Date**, Custom format `MMddHHmm`
   - **Format Date**: Repeat Item → **End Date**, Custom format `MMddHHmm`
   - **Text**: the first Formatted Date, then a hyphen `-`, then the second Formatted Date, with no spaces
3. **End Repeat** → **Combine Text**: Repeat Results, separator **Custom** `.` (a full stop) → **Set Variable** `Sleep`

The dashboard receives every piece of sleep, works out which belong to last night, merges any overlaps so nothing is counted twice, and finds your bedtime and wake time itself.

### Yesterday's activity
Your iPhone and Apple Watch both count steps, and Health merges them so nothing is counted twice. Shortcuts can't do that merge, so it counts each device separately and the dashboard uses the larger number.

4. **Find Health Samples**
   - Type: **Steps**
   - Filter: *Start Date* **is in the last** `1` **days**
   - Filter: *Start Date* **is not today**
   - Filter: *Source* **is** your iPhone (pick it from the list)
   - Group By: **None**
   - → **Calculate Statistics**: **Sum** → **Round Number** (Ones) → **Set Variable** `Steps`
5. Same as step 4, but with *Source* **is** your Apple Watch → **Set Variable** `Steps2`
6. **Find Health Samples**: Type **Active Energy**, *Start Date* **is in the last** `1` **days**, *Start Date* **is not today**, no Source filter, Group By **None** → **Calculate Statistics**: **Sum** → **Round Number** → **Set Variable** `Cal`
7. Same as step 6 with Type **Exercise Minutes** (sometimes listed as *Apple Exercise Time*) → **Set Variable** `Ex`

### Recovery
8. **Find Health Samples**: Type **Heart Rate Variability**, sort by Start Date **Latest First**, **Limit 1** → **Get Details**: Value → **Round Number** → **Set Variable** `HRV`
9. **Find Health Samples**: Type **Resting Heart Rate**, sort **Latest First**, **Limit 1** → **Get Details**: Value → **Round Number** → **Set Variable** `RHR`

### Location (for weather)
10. **Get Current Location** → **Get Details of Locations**: Latitude → **Round Number** (Hundredths) → **Set Variable** `Lat`
11. **Get Current Location** → **Get Details of Locations**: Longitude → **Round Number** (Hundredths) → **Set Variable** `Lon`

### Open the dashboard
12. **Text**: type the link below, all on one line with no spaces. Wherever it shows `[Name]`, delete that and insert the variable with that name from the bar above the keyboard.

```
https://mlthudson14-eng.github.io/dashboard/#sl=[Sleep]&steps=[Steps]&steps2=[Steps2]&cal=[Cal]&ex=[Ex]&rhr=[RHR]&hrv=[HRV]&lat=[Lat]&lon=[Lon]
```

13. **Open URLs** (Text)

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
