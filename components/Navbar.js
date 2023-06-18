"use client";

import React from "react";
import Link from "next/link";
import { useState, useEffect } from "react";

// import { signIn, signOut, useSession, getProviders } from "next-auth/react";

export default function Navbar() {
  //   const { data: session } = useSession();
  //   const [providers, setProviders] = useState(null);

  //   useEffect(() => {
  //     const setupProviders = async () => {
  //       const response = await getProviders();
  //       setProviders(response);
  //     };
  //     setupProviders();
  //   }, []);

  return (
    <div className="flex w-full pt-4 mb-12 flex-col items-center md:flex-row md:justify-between md:px12">
      {/* <div className="flex items-center space-x-8">
        <Link href="/" className="blue-btn">
          Sign up
        </Link>
        {providers &&
          Object.values(providers).map((provider) => (
            <button
              className="blue-btn"
              key={provider.name}
              onClick={() => signIn(providers.id)}
            >
              Sign In
            </button>
          ))}
      </div> */}
    </div>
  );
}
