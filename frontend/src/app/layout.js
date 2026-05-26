import { GeistSans } from "geist/font/sans";
import { GeistMono } from "geist/font/mono";
import { ThemeProvider } from "next-themes";
import "./globals.css";
import { AuthProvider } from "@/contexts/AuthContext";

export const metadata = {
  title: "ResumePilot — AI Employability Intelligence",
  description:
    "The recruiter-grade AI career intelligence platform. Upload your master resume once, and let 75+ specialized engines optimize your trajectory.",
  keywords: [
    "resume",
    "AI",
    "ATS",
    "career intelligence",
    "employability",
    "recruiter",
  ],
  authors: [{ name: "ResumePilot" }],
  openGraph: {
    title: "ResumePilot — AI Employability Intelligence",
    description:
      "Upload your master resume once. Let AI optimize your career trajectory.",
    type: "website",
  },
};

export default function RootLayout({ children }) {
  return (
    <html
      lang="en"
      className={`dark ${GeistSans.variable} ${GeistMono.variable}`}
      suppressHydrationWarning
    >
      <body
        className="font-sans antialiased min-h-screen"
        suppressHydrationWarning
      >
        <ThemeProvider attribute="class" defaultTheme="dark" enableSystem={false}>
          <AuthProvider>{children}</AuthProvider>
        </ThemeProvider>
      </body>
    </html>
  );
}
