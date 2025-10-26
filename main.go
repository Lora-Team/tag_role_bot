package main

import (
	"context"
	"log"
	"os"
	"os/signal"
	"slices"

	"github.com/disgoorg/disgo"
	"github.com/disgoorg/disgo/bot"
	"github.com/disgoorg/disgo/events"
	"github.com/disgoorg/disgo/gateway"
	"github.com/disgoorg/snowflake/v2"
	"github.com/joho/godotenv"
)

func main() {
	err := godotenv.Load()
	if err != nil {
		log.Fatal("Error loading .env file")
	}
	tok := os.Getenv("TOKEN")

	client, err := disgo.New(tok,
		bot.WithDefaultGateway(),
		bot.WithGatewayConfigOpts(
			gateway.WithIntents(
				gateway.IntentGuildMembers,
			),
		),
		bot.WithEventListenerFunc(onReady),
		bot.WithEventListenerFunc(onGuildMemberUpdate),
	)
	if err != nil {
		log.Fatal("Error failed to login into discord!")
	}
	defer client.Close(context.TODO())

	if err = client.OpenGateway(context.TODO()); err != nil {
		log.Fatal("error while connecting to gateway", err.Error())
	}

	// gracefully handle shutdown :)
	sigch := make(chan os.Signal, 1)
	signal.Notify(sigch, os.Interrupt)
	<-sigch

	if err != nil {
		log.Printf("could not close session gracefully: %s", err)
	}
}

func onReady(event *events.Ready) {
	log.Printf("Logged in as %s", event.User.User.Username)
}

func onGuildMemberUpdate(event *events.GuildMemberUpdate) {
	// define role we're working with
	lamp_role := snowflake.ID(1409425360126349483)
	// get conditions we'll use to manage the role
	has_role := slices.Contains(event.Member.RoleIDs, lamp_role)
	has_tag := event.Member.User.PrimaryGuild.Tag != nil && *event.Member.User.PrimaryGuild.Tag == "LAMP"
	// add or remove role based on above conditions
	if has_tag && has_role == false {
		event.Client().Rest.AddMemberRole(event.GuildID, event.Member.User.ID, lamp_role)
		log.Printf("User %s has lamp tag, added role", event.Member.User.Username)
	} else if has_role && has_tag == false {
		event.Client().Rest.RemoveMemberRole(event.GuildID, event.Member.User.ID, lamp_role)
		log.Printf("User %s no longer has lamp tag, removed role", event.Member.User.Username)
	}
}
