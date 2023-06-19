import NextAuth from "next-auth";
import GoogleProvider from "next-auth/providers/google";
import CredentialsProvider from "next-auth/providers/credentials";
import bcrypt from "bcrypt";
import axios from "axios";
import { Pool } from "pg";

const pool = new Pool({
  database: "dbtowerhill",
  user: "dustin",
  password: process.env.DB_PASSWORD,
  host: "dpg-ci7mk0mnqql0ld9b0ch0-a",
  port: 5432,
});

const BASE_URL = "https://towerhill.onrender.com";

const authHandler = NextAuth({
  secret: "IJXvxv2xX79wZ51NAUxxmpUyEQP4aWAkGMkvNtIlP04=",
  providers: [
    GoogleProvider({
      clientId: process.env.GOOGLE_CLIENT_ID,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET_KEY,
    }),

    CredentialsProvider({
      name: "credentials",
      credentials: {
        email: { label: "email", type: "text" },
        password: { label: "password", type: "password" },
      },

      async authorize(credentials, req) {
        if (!credentials.email || !credentials.password) {
          throw new Error("Please enter your email and password");
        }

        // Check to see if user exists
        const user = await fetch(`${BASE_URL}/login`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            email: credentials.email,
            password: credentials.password,
          }),
        });

        if (!user || !user._password_hash) {
          throw new Error("User does not exist");
        }

        // Check to see if password matches
        const passwordMatch = await bcrypt.compare(
          credentials.password,
          user._password_hash
        );

        if (!passwordMatch) {
          throw new Error("Incorrect password");
        }

        return user;
      },
    }),
  ],

  // database: pool,
  session: {
    jwt: true,
  },
  jwt: {
    secret: "kjfdjkiiiiieiemmcm3847883",
  },

  callbacks: {
    async signIn({ profile, user }) {
      if (user) {
        return true;
      }
      try {
        const response = await fetch(`${BASE_URL}/authlogin`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            username: profile.given_name,
            name: profile.name,
            email: profile.email,
            image: profile.picture,
          }),
        });

        const data = await response.json();
        return true;
      } catch (err) {
        console.log(err);
      }
    },
  },

  async session({ session, user }) {
    console.log(session);

    session.user = {
      email: session.user.email,
      name: session.user.name,
      image: session.user.image,
    };
    return session;
  },
});

export { authHandler as GET, authHandler as POST };
