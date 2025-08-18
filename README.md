#  ProperTracker  

This project is a **WhatsApp bot + Property Dashboard** that allows brokers/users to easily upload property listings via WhatsApp. The data is extracted using AI, stored in a Django backend, and displayed on a React + Tailwind frontend dashboard.  

---

## 🚀 Live Links  

- **Backend (Django + Render):** [https://propertracker.onrender.com](https://propertracker.onrender.com)  
- **Frontend (React + Vercel):** [https://proper-tracker.vercel.app/](https://proper-tracker.vercel.app/)  

---

## 📱 How It Works  

1. **Send a message** to this WhatsApp number:  
   -> **`+1 555 145 2717`**
   Important Note on Access:
   Since this project is currently running in test mode, only added tester accounts in the Meta Developer Console can interact with the bot. Messages from non-tester numbers may fail with errors (e.g., 400 Bad       Request)



3. Start by sending a short **description** of the property (e.g., *"2 BHK semi-furnished apartment in Pune for 20,000 INR with 50,000 deposit"*)  

4. The bot will guide you step by step:  
   - Confirm the property upload  
   - Upload multiple images (`Send "DONE"` when finished)  
   - Provide broker name  

5. The details are:  
   - **Extracted by AI** (BHK, furnishing, location, rent, deposit, property type)  
   - **Stored in the backend database**  
   - **Displayed in the property dashboard**  

---

##  Dashboard  

Visit the dashboard here 👉 [Property Dashboard](https://proper-tracker.vercel.app/)  

The dashboard displays:  
- Broker name  
- Description  
- AI-extracted details (BHK, rent, deposit, location, furnishing, property type)  
- Uploaded images (if available)  
- Timestamp of posting  

---

##  Notes  

- The **first response may be slow** because the backend is hosted on **Render Free Tier**.  
  If the server has been inactive, Render spins it down, and it can take **30–60 seconds** to wake up.  
- Please wait if you don’t see an immediate reply from the bot.  

---

## 🛠️ Tech Stack  

- **Backend:** Django, Django REST Framework, LangChain, Pydantic  
- **Frontend:** React.js, Tailwind CSS, Vercel  
- **Database:** PostgreSQL (Render managed)  
- **Messaging:** WhatsApp Business Cloud API  

---

## 📌 Example Flow  

**User:**  
> 2 BHK semi-furnished apartment in Pune available for 20,000 INR rent and 50,000 deposit.  

**Bot:**  
> Do you want to upload this property? (yes/no)  

**User:**  
> yes  

**Bot:**  
> Please upload property images. Send "DONE" when finished.  

**User:**  
> *(uploads images, then types "DONE")*  

**Bot:**  
> Great! Now, under which broker name should I save this?  

**User:**  
> Abhay Realty  

**Bot:**  
> ✅ Property saved  

Now the property appears on the [dashboard](https://proper-tracker.vercel.app/).  

---
