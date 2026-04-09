import { createClient } from "@supabase/supabase-js";

const supabaseUrl =
  process.env.NEXT_PUBLIC_SUPABASE_URL ||
  "https://mewqgevgdgghhatqtuos.supabase.co";

// anon key (공개용, role=anon) — sb_publishable 형식은 supabase-js v2와 호환성 이슈
const supabaseKey =
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY?.startsWith("eyJ")
    ? process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY
    : "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1ld3FnZXZnZGdnaGhhdHF0dW9zIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzI3MTU1MTAsImV4cCI6MjA4ODI5MTUxMH0.sgjPikmLaudwW9iWgg5TQNfSjHVBD7JtjYWgUpNezng";

export const supabase = createClient(supabaseUrl, supabaseKey);
