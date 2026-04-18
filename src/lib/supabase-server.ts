import { createClient } from "@supabase/supabase-js";

const supabaseUrl =
  process.env.SUPABASE_URL ||
  process.env.NEXT_PUBLIC_SUPABASE_URL ||
  "https://mewqgevgdgghhatqtuos.supabase.co";

const supabaseServiceKey =
  process.env.SUPABASE_SERVICE_KEY ||
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY ||
  "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1ld3FnZXZnZGdnaGhhdHF0dW9zIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzI3MTU1MTAsImV4cCI6MjA4ODI5MTUxMH0.sgjPikmLaudwW9iWgg5TQNfSjHVBD7JtjYWgUpNezng";

export const supabaseServer = createClient(supabaseUrl, supabaseServiceKey);
