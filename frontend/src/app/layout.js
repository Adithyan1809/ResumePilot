import { Inter } from "next/font/google";
import "./globals.css";
import { AuthProvider } from "@/contexts/AuthContext";

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
  display: "swap",
});

export const metadata = {
  title: "ResumeAI — AI-Powered Resume Tailoring",
  description:
    "Craft the perfect resume for every job application. AI-powered tailoring, ATS optimization, and intelligent suggestions to land your dream job.",
  keywords: [
    "resume",
    "AI",
    "ATS",
    "job application",
    "career",
    "tailoring",
  ],
  authors: [{ name: "ResumeAI" }],
  openGraph: {
    title: "ResumeAI — AI-Powered Resume Tailoring",
    description:
      "Craft the perfect resume for every job application with AI-powered tailoring.",
    type: "website",
  },
};

export default function RootLayout({ children }) {
  return (
    <html lang="en" className={`dark ${inter.variable}`} suppressHydrationWarning>
      <body className="font-sans antialiased bg-surface-950 text-surface-100 min-h-screen" suppressHydrationWarning>
        <AuthProvider>{children}</AuthProvider>
      </body>
    </html>
  );
}
