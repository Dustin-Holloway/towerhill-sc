"use client";

import {
  ArrowPathIcon,
  CloudArrowUpIcon,
  FingerPrintIcon,
  LockClosedIcon,
} from "@heroicons/react/24/outline";
import { Disclosure, Menu, Transition } from "@headlessui/react";
import { useSession } from "next-auth/react";
import { useState, useEffect } from "react";

export default function MessageBoard() {

  const [messages, setMessages] = useState([]);



    useEffect(() => {
        fetch("https://towerhill-service.onrender.com//messages")
          .then((res) => res.json())
          .then((data) => setMessages(data)
      )}, []);

  


  const [newMessages, setNewMessage] = useState({
    content: "",
  });

  const { data: session, status } = useSession();

  const user = session.user;
  const features = [
    {
      name: "Example title",
      description: "This is the messaging platform, here is sample message.",
    },
  ];

  function handlePost() {



    fetch("/api2/post", {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify(messages),
    })
      .then((res) => res.json())
      .then((data) => {
        console.log(data);
      });
  }

  return (
    <div className="bg-gray-100 py-24 rounded ">
      <div className="mx-auto max-w-5xl px-6 lg:px-8">
        <div className="mx-auto max-w-2xl lg:text-center">
          <h2 className="text-base font-semibold leading-7 text-indigo-600">
            What's going on?
          </h2>
          <p className="mt-2 text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">
            Towerhill messenger.
          </p>
          <p className="mt-6 text-lg leading-8 text-gray-600">
            Leave a message for the community.
          </p>
        </div>
        <div className="flex mx-auto mt-16 max-w-2xl sm:mt-20 lg:mt-24 lg:max-w-4xl ">
          <dl className="py-10 px-10 bg-white rounded-md grid m-auto max-w-xl grid-cols-1 gap-x-5 gap-y-10 lg:max-w-85 justify-center lg:gap-y-10">
            {messages.map((feature) => (
              <div key={feature.id} className="relative pl-16">
                <dt className="text-base font-semibold leading-7 text-gray-900">
                  <div className="absolute left-0 top-0 flex h-10 w-10 items-center justify-center rounded-lg">
                    <div className="flex-shrink-0">
                      <Menu>
                        <Menu.Button className="flex max-w-xs items-center rounded-full bg-gray-800 text-sm focus:outline-none focus:ring-2 focus:ring-white focus:ring-offset-2 focus:ring-offset-gray-800">
                          <img
                            className="h-8 w-8 rounded-full"
                            src={user.image}
                            alt=""
                          />
                        </Menu.Button>
                      </Menu>
                    </div>
                  </div>
                  {feature.comment_type}
                </dt>
                <dd className="mt-2 text-base leading-7 text-gray-600">
                  {feature.content}
                </dd>
              </div>
            ))}

            <div className="flex 1 rounded-md shadow-sm ring-1 ring-inset ring-gray-300 focus-within:ring-2 focus-within:ring-inset focus-within:ring-indigo-600 ">
              <input
                type="text"
                name="content"
                value={...messages.content}
                onChange={(e) => {
                  setMessages({
                    ...messages,
                    [e.target.name]: e.target.value,
                  });
                }}
                className="justify-center mb-1 flex-1 border-0 bg-transparent py-1.5 pl-3 text-gray-900 placeholder:text-gray-400 focus:ring-0 sm:text-sm sm:leading-6"
                placeholder="When did the trash get picked up?"
              />
            </div>
            <button onClick={handlePost} className="flex 1 justify-center  rounded-md p-1 border text-white bg-blue-500">
              Post
            </button>
          </dl>
        </div>
      </div>
    </div>
  );
}
