import NextAuth from "next-auth";
import GoogleProvider from "next-auth/providers/google";
import CredentialsProvider from "next-auth/providers/credentials";
import { useRouter } from "next/navigation";
import { NextResponse } from "next/server";
import bcrypt from "bcrypt";

const authHandler = NextAuth({
  secret: "IJXvxv2xX79wZ51NAUxxmpUyEQP4aWAkGMkvNtIlP04=",
  // session: {
  //   strategy: "jwt",
  // },

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

      async authorize(credentials) {
        // Check to see if the user exists
        if (!credentials.email || !credentials.password) {
          throw new Error("Please enter your email and password");
        }

        // Check to see if user exists
        const response = await fetch("http://127.0.0.1:5555/api2/login", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            email: credentials.email,
            password: credentials.password,
          }),
        });

        const user = await response.json();

        // If no user exists, throw an error
        if (!user || !user?._password_hash) {
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

  callbacks: {
    async signIn({ profile, user }) {
      if (user) {
        return true;
      }
      try {
        const response = await fetch("http://127.0.0.1:5555/api2/authlogin", {
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
